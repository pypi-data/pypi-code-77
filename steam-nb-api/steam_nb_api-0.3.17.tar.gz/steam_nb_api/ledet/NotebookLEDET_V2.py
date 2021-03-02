import os
import copy
import numpy as np
import yaml
import subprocess
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from dataclasses import dataclass, asdict

from steam_nb_api.ledet.ParametersLEDET import ParametersLEDET
from steam_nb_api.ledet.Simulation import RunSimulations
from steam_nb_api.roxie_parser.geometricFunctions import close_pairs_ckdtree, close_pairs_pdist
import sys
import csv
from pathlib import Path
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.lines as lines

from steam_nb_api.ledet.ParametersLEDET import ParametersLEDET
from steam_nb_api.utils import misc
from steam_nb_api.roxie_parser import MagneticCoil
from steam_nb_api.utils.SelfMutualInductanceCalculation import SelfMutualInductanceCalculation

from steam_nb_api.roxie_parser import CableDatabase
from steam_nb_api.roxie_parser import ConductorPosition
from steam_nb_api.roxie_parser.geometricFunctions import close_pairs_ckdtree, close_pairs_pdist

@dataclass
class MagnetGeometry:
    xPos: np.ndarray = np.array([])
    yPos: np.ndarray = np.array([])
    iPos: np.ndarray = np.array([])
    xBarePos: np.ndarray = np.array([])
    yBarePos: np.ndarray = np.array([])
    xS: np.ndarray = np.array([])
    yS: np.ndarray = np.array([])
    iS: np.ndarray = np.array([])
    x: np.ndarray = np.array([])
    y: np.ndarray = np.array([])
    x_ave: np.ndarray = np.array([])
    y_ave: np.ndarray = np.array([])
    x_ave_group: np.ndarray = np.array([])
    y_ave_group: np.ndarray = np.array([])
@dataclass
class MagnetField:
    B: np.ndarray = np.array([])
    Bx: np.ndarray = np.array([])
    By: np.ndarray = np.array([])

def _read_yaml(type_str, elem_name):
    """
    Reads yaml file and returns it as dictionary
    :param type_str: type of file, e.g.: quench, coil, wire
    :param elem_name: file name, e.g. ColSol.1
    :return: dictionary for file named: type.name.yam
    """
    input_folder = os.path.join(os.getcwd(), "Inputs")
    with open(os.path.join(input_folder, f"{type_str}.{elem_name}.yaml"), 'r') as stream:
        data = yaml.safe_load(stream)
    return data

class Notebook_LEDET:
    def __init__(self, nameMagnet):
        # Intrinsic objects
        self.nameMagnet = nameMagnet
        self.Magnet = ParametersLEDET()

        # Miscalleneous
        self.verbose = False
        self.Magnet.Options.headerLines = 1
        self.selectedFont = {'fontname':'DejaVu Sans', 'size':14}
        self.text = {'x': [], 'y': [], 't': []}

        # Start loading
        self.nStrands, self.polarities_inGroup, self.nHalfTurns, self.nTurns, self.nGroups = 0, 0, 0, 0, 0
        self.strandToGroup, self.strandToHalfTurn, self.halfTurnToTurn, self.strandToCoilSection, self.HalfTurnToCoilSection, self.HalfTurnToGroup\
            = np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([])
        [self.MagnetField, self.MagnetGeometry] = self._load_ROXIE()
        self.load_MagnetData()

        self.Magnet.Inputs.GroupToCoilSection = int(self.nGroups) * [1] ## !!!TODO

        return

    def set(self, key, values):

        if key in self.Magnet.Inputs.__annotations__:
            sheet = 'Inputs'
        if key in self.Magnet.Options.__annotations__:
            sheet = 'Options'
        if key in self.Magnet.Plots.__annotations__:
            sheet = 'Plots'
        if key in self.Magnet.Variables.__annotations__:
            sheet = 'Variables'

    def _load_ROXIE(self):
        # Select ROXIE .cadata file with conductor data
        currentDirectory = Path(os.path.split(os.getcwd())[0])
        fileNameCadata = os.path.join(currentDirectory, 'resources', 'roxie_parser', 'roxie.cadata')
        fileName = self.nameMagnet + '_All_WithIron_WithSelfField.map2d'
        fileNameData = self.nameMagnet + '_All_WithIron_WithSelfField.data'

        strandToGroup = np.array([])
        strandToHalfTurn = np.array([])
        idx = []
        x = []
        y = []
        Bx = []
        By = []
        Area = []
        I = []
        fillFactor = []

        # Read file
        file = open(fileName, "r")
        fileContent = file.read()
        # Separate rows
        fileContentByRow = fileContent.split("\n")

        for index in range(len(fileContentByRow) - 1):
            if index > self.Magnet.Options.headerLines:
                fc = fileContentByRow[index]
                row = fc.split()
                strandToGroup = np.hstack([strandToGroup, int(row[0])])
                strandToHalfTurn = np.hstack([strandToHalfTurn, int(row[1])])
                idx = np.hstack([idx, float(row[2])])
                x = np.hstack([x, float(row[3]) / 1000])  # in [m]
                y = np.hstack([y, float(row[4]) / 1000])  # in [m]
                Bx = np.hstack([Bx, float(row[5])])
                By = np.hstack([By, float(row[6])])
                Area = np.hstack([Area, float(row[7])])
                I = np.hstack([I, float(row[8])])
                fillFactor = np.hstack([fillFactor, float(row[9])])
        [_, c] = np.unique(strandToHalfTurn, return_index=True)
        [_, self.Magnet.Inputs.nT] = np.unique(strandToGroup[c], return_counts=True)
        self.Magnet.Inputs.nStrands_inGroup = np.gradient(c)[np.cumsum(self.Magnet.Inputs.nT)-1]

        nStrandsFieldMap = len(strandToGroup)
        if self.verbose: print('Total number of strands in the field-map from ROXIE = {}'.format(nStrandsFieldMap))

        # Calculate absolute magnetic field
        B = []
        for i in range(nStrandsFieldMap):
            B = np.hstack([B, (Bx[i] ** 2 + By[i] ** 2) ** .5])
        Bfield = MagnetField(B, Bx, By)
        if self.verbose: print('Peak magnetic field in the field-map from ROXIE = {} T'.format(np.max(B)))

        # Number of strands in each half-turn
        self.nStrands = len(strandToGroup)
        self.Magnet.Inputs.polarities_inGroup = np.sign(I[c])[np.cumsum(self.Magnet.Inputs.nT)-1]
        self.nHalfTurns = int(np.max(strandToHalfTurn))
        self.nTurns = int(self.nHalfTurns / 2)
        self.nGroups = int(np.max(strandToGroup))

        self.strandToGroup = np.int_(strandToGroup)
        self.strandToHalfTurn = np.int_(strandToHalfTurn)
        self.halfTurnToTurn = np.tile(np.arange(1, self.nTurns + 1), 2)

        # Average half-turn positions
        x_ave = []
        y_ave = []
        for ht in range(1, self.nHalfTurns + 1):
            x_ave = np.hstack([x_ave, np.mean(x[np.where(self.strandToHalfTurn == ht)])])
            y_ave = np.hstack([y_ave, np.mean(y[np.where(self.strandToHalfTurn == ht)])])

        # Average group positions
        x_ave_group = []
        y_ave_group = []
        for g in range(1, self.nGroups + 1):
            x_ave_group = np.hstack([x_ave_group, np.mean(x[np.where(self.strandToGroup == g)])])
            y_ave_group = np.hstack([y_ave_group, np.mean(y[np.where(self.strandToGroup == g)])])

        if self.verbose:
            print('Total number of strands = ' + str(self.nStrands))
            print('Total number of half-turns = ' + str(self.nHalfTurns))
            print('Total number of turns = ' + str(self.nTurns))
            print('Total number of groups = ' + str(self.nGroups))

        # Define the magnetic coil
        definedMagneticCoil = MagneticCoil.MagneticCoil()
        xPos, yPos, iPos, xBarePos, yBarePos, xS, yS, iS = \
            definedMagneticCoil.generateCoilGeometry(fileNameData, fileNameCadata, verbose = self.verbose)
        MagnetGeo = MagnetGeometry(xPos, yPos, iPos, xBarePos, yBarePos, xS, yS, iS, x, y, x_ave, y_ave, x_ave_group, y_ave_group)
        return [Bfield, MagnetGeo]

    def load_MagnetData(self):
        ## T00, I0, l_magnet, Iref
        magnet_data = _read_yaml('magnet', self.nameMagnet)

        for key in magnet_data.keys():
            if key in self.Magnet.Inputs.__annotations__:
                self.Magnet.setAttribute('Inputs', key, magnet_data[key])
            if key in self.Magnet.Options.__annotations__:
                self.Magnet.setAttribute('Options', key, magnet_data[key])

        self.Magnet.Inputs.l_mag_inGroup = np.ones((self.nGroups,))*self.Magnet.Inputs.l_magnet
        return

    def load_ConductorData(self, Conductor):
        conductor_data = _read_yaml('conductor', Conductor)
        for key in conductor_data.keys():
            if key in self.Magnet.Inputs.__annotations__:
                Values = np.array([float(conductor_data[key])] * self.nGroups)
                self.Magnet.setAttribute('Inputs', key, Values)
        try:
            self.Magnet.Options.fScaling_Pex_AlongHeight_Defined = (2 *  conductor_data['insulationAroundCables']) / (
                        2 *  conductor_data['insulationAroundCables'] +  conductor_data['insulationBetweenLayers'])
        except:
            self.Magnet.Options.fScaling_Pex_AlongHeight_Defined = 1
            pass

        self.__calculateSelfMutualInductance()
        return

    def load_Options(self, Type):
        if Type=='Default':
            option_data = _read_yaml('options', Type)
            for key in option_data.keys():
                if key in self.Magnet.Options.__annotations__:
                    Values = option_data[key]
                    self.Magnet.setAttribute('Options', key, Values)
        else:
            print('Option type ', Type, ' currently not supported or not understood.')

    def set_ElectricalOrder(self, elPairs_GroupTogether, elPairs_RevElOrder):
        # Start and end indices of each group
        indexTstop = np.cumsum(self.Magnet.Inputs.nT)
        indexTstop = indexTstop.tolist()
        indexTstart = [1]
        for i in range(len(self.Magnet.Inputs.nT) - 1):
            indexTstart.extend([indexTstart[i] + self.Magnet.Inputs.nT[i]])

        nElPairs = len(elPairs_GroupTogether)
        if self.verbose:
            print('The half-turns of these pairs of groups will be connected electrically:')
            print(elPairs_GroupTogether)

        if len(elPairs_RevElOrder) != nElPairs:
            raise Exception('Length of the vector elPairs_RevElOrder ({}) must be equal to nElPairs={}.'.format(
                len(elPairs_RevElOrder), nElPairs))

        el_order_half_turns = []
        for p in range(nElPairs):
            if self.Magnet.Inputs.nT[elPairs_GroupTogether[p][0] - 1] != self.Magnet.Inputs.nT[elPairs_GroupTogether[p][1] - 1]:
                raise Exception(
                    'Pair of groups defined by the variable elPairs_GroupTogether must have the same number of half-turns.')
            for k in range(self.Magnet.Inputs.nT[elPairs_GroupTogether[p][0] - 1]):
                if elPairs_RevElOrder[p] == 0:
                    el_order_half_turns.append(indexTstart[elPairs_GroupTogether[p][0] - 1] + k)
                    el_order_half_turns.append(indexTstart[elPairs_GroupTogether[p][1] - 1] + k)
                if elPairs_RevElOrder[p] == 1:
                    el_order_half_turns.append(indexTstop[elPairs_GroupTogether[p][0] - 1] - k)
                    el_order_half_turns.append(indexTstop[elPairs_GroupTogether[p][1] - 1] - k)

        self.Magnet.Inputs.el_order_half_turns = np.array(el_order_half_turns)

    def set_ThermalConnections(self, max_distance):
        # Start and end indices of each group
        indexTstop = np.cumsum(self.Magnet.Inputs.nT)
        indexTstop = indexTstop.tolist()
        indexTstart = [1]
        for i in range(len(self.Magnet.Inputs.nT) - 1):
            indexTstart.extend([indexTstart[i] + self.Magnet.Inputs.nT[i]])

        iContactAlongWidth_From = []
        iContactAlongWidth_To = []

        for g in range(self.nGroups):
            iContactAlongWidth_From.extend(range(indexTstart[g], indexTstop[g]))
            iContactAlongWidth_To.extend(range(indexTstart[g] + 1, indexTstop[g] + 1))

        self.Magnet.Inputs.iContactAlongWidth_From = np.array(iContactAlongWidth_From)
        self.Magnet.Inputs.iContactAlongWidth_To = np.array(iContactAlongWidth_To)

        if self.verbose:
            print('Heat exchange along the cable wide side - Calculated indices:')
            print('iContactAlongWidth_From = ')
            print(iContactAlongWidth_From)
            print('iContactAlongWidth_To = ')
            print(iContactAlongWidth_To)

        # Prepare input for the function close_pairs_ckdtree
        X = np.column_stack((self.MagnetGeometry.x, self.MagnetGeometry.y))

        # find all pairs of strands closer than a distance of max_d
        pairs_close = close_pairs_ckdtree(X, max_distance)

        # find pairs that belong to half-turns located in different groups
        contact_pairs = set([])
        for p in pairs_close:
            if not self.strandToGroup[p[0]] == self.strandToGroup[p[1]]:
                contact_pairs.add((self.strandToHalfTurn[p[0]], self.strandToHalfTurn[p[1]]))

        # assign the pair values to two distinct vectors
        iContactAlongHeight_From = []
        iContactAlongHeight_To = []
        for p in contact_pairs:
            iContactAlongHeight_From.append(p[0])
            iContactAlongHeight_To.append(p[1])
        # Keep arrays Non-empty
        iContactAlongHeight_From.append(1)
        iContactAlongHeight_To.append(1)

        # find indices to order the vector iContactAlongHeight_From
        idxSort = [i for (v, i) in sorted((v, i) for (i, v) in enumerate(iContactAlongHeight_From))]

        # reorder both iContactAlongHeight_From and iContactAlongHeight_To using the indices
        self.Magnet.Inputs.iContactAlongHeight_From = [iContactAlongHeight_From[i] for i in idxSort]
        self.Magnet.Inputs.iContactAlongHeight_To = [iContactAlongHeight_To[i] for i in idxSort]

        if self.verbose:
            print('Heat exchange along the cable narrow side - Calculated indices:')
            print('iContactAlongHeight_From = ')
            print(self.Magnet.Inputs.iContactAlongHeight_From)
            print('iContactAlongWidth_To = ')
            print(self.Magnet.Inputs.iContactAlongHeight_To)

    def set_QuenchScenario(self, Scenario):
        if Scenario == '2D+1D':
            self.Magnet.Inputs.iStartQuench = np.linspace(1,self.nHalfTurns, self.nHalfTurns)
            self.Magnet.Inputs.tStartQuench = np.ones((self.nHalfTurns,))*9999
            self.Magnet.Inputs.lengthHotSpot_iStartQuench = np.ones((self.nHalfTurns,))*0.01
            ROXIE_File = self.nameMagnet + '_All_WithIron_WithSelfField.map2d'
            self.Magnet.adjust_vQ(ROXIE_File)
        else:
            print('Scenario ', Scenario, ' currently not supported or not understood.')

    def __calculateSelfMutualInductance(self):
        # Self-mutual inductance calculation, using SMIC (https://cernbox.cern.ch/index.php/s/37F87v3oeI2Gkp3)
        flag_strandCorrection = 0
        flag_sumTurnToTurn = 1
        flag_writeOutput = 0

        # Calculate group to which each half-turn belongs
        indexTstart = np.hstack([1, 1 + np.cumsum(self.Magnet.Inputs.nT[:-1])])
        indexTstop = np.cumsum(self.Magnet.Inputs.nT)
        HalfTurnToGroup = np.zeros((1, self.nHalfTurns), dtype=int)
        HalfTurnToGroup = HalfTurnToGroup[0]
        HalfTurnToCoilSection = np.zeros((1, self.nHalfTurns), dtype=int)
        HalfTurnToCoilSection = HalfTurnToCoilSection[0]
        for g in range(1, self.nGroups + 1):
            HalfTurnToGroup[indexTstart[g - 1] - 1:indexTstop[g - 1]] = g
            HalfTurnToCoilSection[indexTstart[g - 1] - 1:indexTstop[g - 1]] = self.Magnet.Inputs.GroupToCoilSection[g - 1]

        # Calculate group to which each strand belongs
        nS = np.repeat(self.Magnet.Inputs.nStrands_inGroup, self.Magnet.Inputs.nT)
        indexSstart = np.hstack([1, 1 + np.cumsum(nS[:-1])]).astype(int)
        indexSstop = np.cumsum(nS).astype(int)
        strandToGroup = np.zeros((1, self.nStrands), dtype=int)
        strandToGroup = strandToGroup[0]
        strandToCoilSection = np.zeros((1, self.nStrands), dtype=int)
        strandToCoilSection = strandToCoilSection[0]
        for ht in range(1, self.nHalfTurns + 1):
            strandToGroup[indexSstart[ht - 1] - 1:indexSstop[ht - 1]] = HalfTurnToGroup[ht - 1]
            strandToCoilSection[indexSstart[ht - 1] - 1:indexSstop[ht - 1]] = HalfTurnToCoilSection[ht - 1]

        polarities = np.repeat(self.Magnet.Inputs.polarities_inGroup, self.Magnet.Inputs.nT)
        polarities = np.repeat(polarities, nS.astype(int))
        for i in range(2):
            # Calculate diameter of each strand
            Ds = np.zeros((1, self.nStrands), dtype=float)
            Ds = Ds[0]
            for g in range(1, self.nGroups + 1):
                if i == 0: Ds[np.where(strandToGroup == g)] = self.Magnet.Inputs.ds_inGroup[g - 1]
                if i == 1: Ds[np.where(strandToGroup == g)] = self.Magnet.Inputs.hBare_inGroup[g - 1]

            # Define self-mutual inductance calculation object
            coil = SelfMutualInductanceCalculation(self.MagnetGeometry.x, self.MagnetGeometry.y, polarities,
                                                   nS, Ds, self.strandToHalfTurn, strandToCoilSection,
                                                   flag_strandCorrection, flag_sumTurnToTurn, flag_writeOutput,
                                                   self.nameMagnet)

            # Calculate self-mutual inductance between half-turns, turns, and coil-sections, per unit length [H/m]
            M_halfTurns_calculated, M_turns_calculated, M_coilSections_calculated, L_mag0_calculated = \
                coil.calculateInductance(self.MagnetGeometry.x, self.MagnetGeometry.y, polarities,
                                         nS, Ds, self.strandToHalfTurn, strandToCoilSection,
                                         flag_strandCorrection=0)

            L_turns = M_turns_calculated
            L_turns_diag = np.diagonal(L_turns)
            L_turns_diag_rep = np.tile(L_turns_diag, (len(L_turns),
                                                      1))  # this replicates the effect of L_xx[i][i]
            denom_turns = np.sqrt(L_turns_diag_rep.T * L_turns_diag_rep)
            k_turns = L_turns / denom_turns  # matrix alt to k_turns[i][j]=L_turns[i][j]/np.sqrt(L_turns[j][j]*L_turns[i][i])

            if len(k_turns[np.where(k_turns > 1)]) == 0:
                break
            else:
                assert max(self.Magnet.Inputs.nStrands_inGroup) == 1, 'Wires are not single stranded but k>1'
                print('Mutual inductance of some turns is k>1, re-calculate with hBare.')

        self.strandToCoilSection = strandToCoilSection
        self.HalfTurnToCoilSection = HalfTurnToCoilSection
        self.HalfTurnToGroup = HalfTurnToGroup

        # Self-mutual inductances between coil sections, per unit length [H/m]
        self.Magnet.Inputs.M_m = M_coilSections_calculated
        # Self-mutual inductances between turns, per unit length [H/m]
        self.Magnet.Inputs.M_InductanceBlock_m = M_turns_calculated
        # Total magnet self-mutual inductance, per unit length [H/m]
        L_mag0 = L_mag0_calculated

        if self.verbose:
            print('')
            print('Total magnet self-inductance per unit length: ' + str(L_mag0) + ' H/m')

        # Check if Self-mutual inductance is too large
        if self.Magnet.Inputs.M_InductanceBlock_m.shape[0] >= 50:
            if self.verbose: print('Write Inductance matrix to csv')
            with open(self.nameMagnet + '_selfMutualInductanceMatrix.csv', 'w') as file:
                reader = csv.writer(file)
                reader.writerow(["Extended self mutual inductance matrix [H/m]"])
                for i in range(self.Magnet.Inputs.M_InductanceBlock_m.shape[0]):
                    reader.writerow(self.Magnet.Inputs.M_InductanceBlock_m[i])
            self.Magnet.Inputs.M_InductanceBlock_m = np.array([0])

    ## Plotting part
    def plotter(self, data, titles, labels, types, texts, size):
        """
        Default plotter for most standard and simple cases
        """
        fig, axs = plt.subplots(nrows=1, ncols=len(data), figsize=size)
        if len(data) == 1:
            axs = [axs]
        for ax, ty, d, ti, l, te in zip(axs, types, data, titles, labels, texts):
            if ty == 'scatter':
                plot = ax.scatter(d['x'], d['y'], s=2, c=d['z'], cmap='jet')  # =cm.get_cmap('jet'))
                if len(te["t"]) != 0:
                    for x, y, z in zip(te["x"], te["y"], te["t"]):
                        ax.text(x, y, z)
            elif ty == 'plot':
                pass  # TODO make non scatter plots work. Some of non-scater plots are quite specific. Might be better off with a separate plotter
            ax.set_xlabel(l["x"], **self.selectedFont)
            ax.set_ylabel(l["y"], **self.selectedFont)
            ax.set_title(f'{ti}', **self.selectedFont)
            # ax.set_aspect('equal')
            # ax.figure.autofmt_xdate()
            cax = make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05)
            cbar = fig.colorbar(plot, cax=cax, orientation='vertical')
            if len(l["z"]) != 0:
                cbar.set_label(l["z"], **self.selectedFont)
        plt.tight_layout()
        plt.show()

    def plot_field(self):
        """
        Plot magnetic field components of a coil
        """
        I = np.repeat(self.Magnet.Inputs.polarities_inGroup, self.Magnet.Inputs.nT)
        nS = np.repeat(self.Magnet.Inputs.nStrands_inGroup, self.Magnet.Inputs.nT)
        I = np.repeat(I, nS.astype(int)) *self.Magnet.Inputs.I00

        data = [{'x': self.MagnetGeometry.x, 'y': self.MagnetGeometry.y, 'z': I},
                {'x': self.MagnetGeometry.x, 'y': self.MagnetGeometry.y, 'z': self.MagnetField.Bx},
                {'x': self.MagnetGeometry.x, 'y': self.MagnetGeometry.y, 'z': self.MagnetField.By},
                {'x': self.MagnetGeometry.x, 'y': self.MagnetGeometry.y, 'z': self.MagnetField.B}]
        titles = ['Current [A]', 'Br [T]', 'Bz [T]', 'Bmod [T]']
        labels = [{'x': "r (m)", 'y': "z (m)", 'z': ""}] * len(data)
        types = ['scatter'] * len(data)
        texts = [self.text] * len(data)
        self.plotter(data, titles, labels, types, texts, (15, 5))

    def plot_strands_groups_layers(self):
        types = ['scatter'] * 4
        data = [{'x': self.MagnetGeometry.x, 'y': self.MagnetGeometry.y, 'z': self.strandToHalfTurn},
                {'x': self.MagnetGeometry.x, 'y': self.MagnetGeometry.y, 'z': self.strandToGroup},
                {'x': self.MagnetGeometry.x_ave, 'y': self.MagnetGeometry.y_ave, 'z': self.halfTurnToTurn},
                {'x': self.MagnetGeometry.x_ave, 'y': self.MagnetGeometry.y_ave, 'z': np.repeat(self.Magnet.Inputs.nStrands_inGroup, self.Magnet.Inputs.nT)}]
        titles = ['strandToHalfTurn', 'strandToGroup', 'halfTurnToTurn', 'Number of strands per half-turn']
        labels = [{'x': "r (m)", 'y': "z (m)", 'z': "Half-turn [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Group [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Turn [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Number of  strands per cable [-]"}]
        t_ht = copy.deepcopy(self.text)
        for ht in range(self.nHalfTurns):
            t_ht['x'].append(self.MagnetGeometry.x_ave[ht])
            t_ht['y'].append(self.MagnetGeometry.y_ave[ht])
            t_ht['t'].append('{}'.format(ht + 1))
        t_ng = copy.deepcopy(self.text)
        for g in range(self.nGroups):
            t_ng['x'].append(self.MagnetGeometry.x_ave_group[g])
            t_ng['y'].append(self.MagnetGeometry.y_ave_group[g])
            t_ng['t'].append('{}'.format(g + 1))
        texts = [t_ht, t_ng, self.text, self.text]
        self.plotter(data, titles, labels, types, texts, (15, 5))

    def plot_polarities(self):
        polarities_inStrand = np.zeros((1, self.nStrands), dtype=int)
        polarities_inStrand = polarities_inStrand[0]
        for g in range(1, self.nGroups+ 1):
            polarities_inStrand[np.where(self.strandToGroup == g)] = self.Magnet.Inputs.polarities_inGroup[g - 1]
        data = [{'x': self.MagnetGeometry.x, 'y': self.MagnetGeometry.y, 'z': polarities_inStrand}]
        titles = ['Current polarities']
        labels = [{'x': "r (m)", 'y': "z (m)", 'z': "Polarity [-]"}]
        types = ['scatter'] * len(data)
        texts = [self.text] * len(data)
        self.plotter(data, titles, labels, types, texts, (5, 5))

    def plot_half_turns(self):
        data = [{'x': self.MagnetGeometry.x_ave, 'y': self.MagnetGeometry.y_ave, 'z': self.HalfTurnToGroup},
                {'x': self.MagnetGeometry.x_ave, 'y': self.MagnetGeometry.y_ave, 'z': self.HalfTurnToCoilSection},
                {'x': self.MagnetGeometry.x, 'y': self.MagnetGeometry.y, 'z': self.strandToGroup},
                {'x': self.MagnetGeometry.x, 'y': self.MagnetGeometry.y, 'z': self.strandToCoilSection}]
        titles = ['HalfTurnToGroup', 'HalfTurnToCoilSection', 'StrandToGroup', 'StrandToCoilSection']
        labels = [{'x': "r (m)", 'y': "z (m)", 'z': "Group [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Coil section [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Group [-]"},
                  {'x': "r (m)", 'y': "z (m)", 'z': "Coil Section [-]"}]
        types = ['scatter'] * len(data)
        texts = [self.text] * len(data)
        self.plotter(data, titles, labels, types, texts, (15, 5))

    def plot_nonlin_induct(self):
        f = plt.figure(figsize=(7.5, 5))
        plt.plot(self.Magnet.Inputs.fL_I, self.Magnet.Inputs.fL_L, 'ro-')
        plt.xlabel('Current [A]', **self.selectedFont)
        plt.ylabel('Factor scaling nominal inductance [-]', **self.selectedFont)
        plt.title('Differential inductance versus current', **self.selectedFont)
        plt.xlim([0, self.Magnet.Inputs.I00 * 2])
        plt.grid(True)
        plt.rcParams.update({'font.size': 12})
        plt.show()

    def plot_psu_and_trig(self):
        # Plot
        f = plt.figure(figsize=(7.5, 5))
        plt.plot([self.Magnet.Inputs.t_PC, self.Magnet.Inputs.t_PC], [0, 1], 'k--', linewidth=4.0, label='t_PC')
        plt.plot([self.Magnet.Inputs.tEE, self.Magnet.Inputs.tEE], [0, 1], 'r--', linewidth=4.0, label='t_EE')
        plt.plot([self.Magnet.Inputs.tCLIQ, self.Magnet.Inputs.tCLIQ], [0, 1], 'g--', linewidth=4.0, label='t_CLIQ')
        plt.plot([np.min(self.Magnet.Inputs.tQH), np.min(self.Magnet.Inputs.tQH)], [0, 1], 'b:', linewidth=2.0, label='t_QH')
        plt.xlabel('Time [s]', **self.selectedFont)
        plt.ylabel('Trigger [-]', **self.selectedFont)
        plt.xlim([1E-4, self.Magnet.Options.time_vector_params[-1]])
        plt.title('Power suppply and quench protection triggers', **self.selectedFont)
        plt.grid(True)
        plt.rcParams.update({'font.size': 12})
        plt.legend(loc='best')
        plt.tight_layout()
        plt.show()

    def plot_quench_prop_and_resist(self):
        # Calculate resistance of each turn at T=10 K
        rho_Cu_10K = 1.7E-10  # [Ohm*m] Approximate Cu resistivity at T=10 K, B=0, for RRR=100
        rho_Cu_10K_B = 4E-11  # [Ohm*m/T] Approximate Cu magneto-resistivity factor
        uQuenchDetectionThreshold = 0.1
        rho_ht_10K = []
        r_el_ht_10K = []
        mean_B_ht = []
        tQuenchDetection = []
        for ht in range(1, self.nHalfTurns + 1):
            current_group = self.HalfTurnToGroup[ht - 1]
            mean_B = np.mean(
                self.MagnetField.B[np.where(
                    self.strandToHalfTurn == ht)]) / self.Magnet.Options.Iref * self.Magnet.Inputs.I00  # average magnetic field in the current half-turn
            rho_mean = rho_Cu_10K + rho_Cu_10K_B * mean_B  # average resistivity in the current half-turn
            cross_section = self.Magnet.Inputs.nStrands_inGroup[current_group - 1] * np.pi / 4 * self.Magnet.Inputs.ds_inGroup[
                current_group - 1] ** 2 * (1 - self.Magnet.Inputs.f_SC_strand_inGroup[current_group - 1])
            r_el_m = rho_mean / cross_section  # Electrical resistance per unit length
            tQD = uQuenchDetectionThreshold / (self.Magnet.Inputs.vQ_iStartQuench[
                                                        ht - 1] * r_el_m * self.Magnet.Inputs.I00)  # Approximate time to reach the quench detection threshold
            mean_B_ht = np.hstack([mean_B_ht, mean_B])
            rho_ht_10K = np.hstack([rho_ht_10K, rho_mean])
            r_el_ht_10K = np.hstack([r_el_ht_10K, r_el_m])
            tQuenchDetection = np.hstack([tQuenchDetection, tQD])


        f = plt.figure(figsize=(16, 6))
        plt.subplot(1, 4, 1)
        # fig, ax = plt.subplots()
        plt.scatter(self.MagnetGeometry.x_ave * 1000, self.MagnetGeometry.y_ave * 1000, s=2, c=self.Magnet.Inputs.vQ_iStartQuench)
        plt.xlabel('x [mm]', **self.selectedFont)
        plt.ylabel('y [mm]', **self.selectedFont)
        plt.title('2D cross-section Quench propagation velocity', **self.selectedFont)
        plt.set_cmap('jet')
        plt.grid('minor', alpha=0.5)
        cbar = plt.colorbar()
        cbar.set_label('Quench velocity [m/s]', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        # plt.axis('equal')

        plt.subplot(1, 4, 2)
        plt.scatter(self.MagnetGeometry.x_ave * 1000, self.MagnetGeometry.y_ave * 1000, s=2, c=rho_ht_10K)
        plt.xlabel('x [mm]', **self.selectedFont)
        plt.ylabel('y [mm]', **self.selectedFont)
        plt.title('Resistivity', **self.selectedFont)
        plt.set_cmap('jet')
        plt.grid('minor', alpha=0.5)
        cbar = plt.colorbar()
        cbar.set_label('Resistivity [$\Omega$*m]', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        # plt.axis('equal')

        plt.subplot(1, 4, 3)
        plt.scatter(self.MagnetGeometry.x_ave * 1000, self.MagnetGeometry.y_ave * 1000, s=2, c=r_el_ht_10K)
        plt.xlabel('x [mm]', **self.selectedFont)
        plt.ylabel('y [mm]', **self.selectedFont)
        plt.title('Resistance per unit length', **self.selectedFont)
        plt.set_cmap('jet')
        plt.grid('minor', alpha=0.5)
        cbar = plt.colorbar()
        cbar.set_label('Resistance per unit length [$\Omega$/m]', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        # plt.axis('equal')

        plt.subplot(1, 4, 4)
        plt.scatter(self.MagnetGeometry.x_ave * 1000, self.MagnetGeometry.y_ave * 1000, s=2, c=tQuenchDetection * 1e3)
        plt.xlabel('x [mm]', **self.selectedFont)
        plt.ylabel('y [mm]', **self.selectedFont)
        plt.title('Approximate quench detection time', **self.selectedFont)
        plt.set_cmap('jet')
        plt.grid('minor', alpha=0.5)
        cbar = plt.colorbar()
        cbar.set_label('Time [ms]', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        # plt.axis('equal')
        plt.show()

    def plot_electrical_order(self):
        plt.figure(figsize=(16, 8))
        plt.subplot(1, 3, 1)
        plt.scatter(self.MagnetGeometry.x_ave, self.MagnetGeometry.y_ave, s=2, c=np.argsort(self.Magnet.Inputs.el_order_half_turns))
        plt.xlabel('x [m]', **self.selectedFont)
        plt.ylabel('y [m]', **self.selectedFont)
        plt.title('Electrical order of the half-turns', **self.selectedFont)
        plt.set_cmap('jet')
        cbar = plt.colorbar()
        cbar.set_label('Electrical order [-]', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        plt.axis('equal')
        # Plot
        plt.subplot(1, 3, 2)
        plt.plot(self.MagnetGeometry.x_ave[self.Magnet.Inputs.el_order_half_turns - 1],
                 self.MagnetGeometry.y_ave[self.Magnet.Inputs.el_order_half_turns - 1], 'k')
        plt.scatter(self.MagnetGeometry.x_ave, self.MagnetGeometry.y_ave, s=2, c=np.repeat(self.Magnet.Inputs.nStrands_inGroup, self.Magnet.Inputs.nT))
        plt.scatter(self.MagnetGeometry.x_ave[self.Magnet.Inputs.el_order_half_turns[0] - 1],
                    self.MagnetGeometry.y_ave[self.Magnet.Inputs.el_order_half_turns[0] - 1], s=50, c='r',
                    label='Positive lead')
        plt.scatter(self.MagnetGeometry.x_ave[self.Magnet.Inputs.el_order_half_turns[-1] - 1],
                    self.MagnetGeometry.y_ave[self.Magnet.Inputs.el_order_half_turns[-1] - 1], s=50, c='b',
                    label='Negative lead')
        plt.xlabel('x [m]', **self.selectedFont)
        plt.ylabel('y [m]', **self.selectedFont)
        plt.title('Electrical order of the half-turns', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        plt.axis('equal')
        plt.legend(loc='lower left')
        # Plot
        plt.subplot(1, 3, 3)
        # plt.plot(x_ave_group[elPairs_GroupTogether_Array[:,0]-1],y_ave_group[elPairs_GroupTogether_Array[:,1]-1],'b')
        plt.scatter(self.MagnetGeometry.x, self.MagnetGeometry.y, s=2, c='k')
        plt.scatter(self.MagnetGeometry.x_ave_group, self.MagnetGeometry.y_ave_group, s=10, c='r')
        plt.xlabel('x [m]', **self.selectedFont)
        plt.ylabel('y [m]', **self.selectedFont)
        plt.title('Electrical order of the groups (only go-lines)', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        plt.axis('equal')
        plt.show()

    def plot_heat_exchange_order(self):
        plt.figure(figsize=(10, 10))
        # plot strand positions
        plt.scatter(self.MagnetGeometry.x, self.MagnetGeometry.y, s=2, c='b')
        # plot conductors
        # for c, (cXPos, cYPos) in enumerate(zip(xPos, yPos)):
        #     pt1, pt2, pt3, pt4 = (cXPos[0], cYPos[0]), (cXPos[1], cYPos[1]), (cXPos[2], cYPos[2]), (cXPos[3], cYPos[3])
        #     line = plt.Polygon([pt1, pt2, pt3, pt4], closed=True, fill=True, facecolor='r', edgecolor='k', alpha=.25)
        #     plt.gca().add_line(line)
        # plot average conductor positions
        # plt.scatter(x_ave, y_ave, s=10, c='r')
        # plot heat exchange links along the cable narrow side
        for i in range(len(self.Magnet.Inputs.iContactAlongHeight_From)):
            plt.plot([self.MagnetGeometry.x_ave[self.Magnet.Inputs.iContactAlongHeight_From[i] - 1],
                      self.MagnetGeometry.x_ave[self.Magnet.Inputs.iContactAlongHeight_To[i] - 1]],
                     [self.MagnetGeometry.y_ave[self.Magnet.Inputs.iContactAlongHeight_From[i] - 1],
                      self.MagnetGeometry.y_ave[self.Magnet.Inputs.iContactAlongHeight_To[i] - 1]], 'k')
        # plot heat exchange links along the cable wide side
        for i in range(len(self.Magnet.Inputs.iContactAlongWidth_From)):
            plt.plot([self.MagnetGeometry.x_ave[self.Magnet.Inputs.iContactAlongWidth_From[i] - 1],
                      self.MagnetGeometry.x_ave[self.Magnet.Inputs.iContactAlongWidth_To[i] - 1]],
                     [self.MagnetGeometry.y_ave[self.Magnet.Inputs.iContactAlongWidth_From[i] - 1],
                      self.MagnetGeometry.y_ave[self.Magnet.Inputs.iContactAlongWidth_To[i] - 1]], 'r')
        # plot strands belonging to different conductor groups and clo ser to each other than max_distance
        # for p in pairs_close:
        #     if not strandToGroup[p[0]] == strandToGroup[p[1]]:
        #         plt.plot([X[p[0], 0], X[p[1], 0]], [X[p[0], 1], X[p[1], 1]], c='g')
        plt.xlabel('x [m]', **self.selectedFont)
        plt.ylabel('y [m]', **self.selectedFont)
        plt.title('Heat exchange order of the half-turns', **self.selectedFont)
        plt.rcParams.update({'font.size': 12})
        plt.axis('equal')
        plt.show()

    def plot_power_supl_contr(self):
        plt.figure(figsize=(5, 5))
        plt.plot([self.Magnet.Inputs.t_PC, self.Magnet.Inputs.t_PC], [np.min(self.Magnet.Inputs.I_PC_LUT), np.max(self.Magnet.Inputs.I_PC_LUT)], 'k--', linewidth=4.0,
                 label='t_PC')
        plt.plot(self.Magnet.Inputs.t_PC_LUT, self.Magnet.Inputs.I_PC_LUT, 'ro-', label='LUT')
        plt.xlabel('Time [s]', **self.selectedFont)
        plt.ylabel('Current [A]', **self.selectedFont)
        plt.title('Look-up table controlling power supply', **self.selectedFont)
        plt.grid(True)
        plt.rcParams.update({'font.size': 12})
        plt.show()

    def plot_all(self):
        self.plot_field()
        self.plot_polarities()
        self.plot_strands_groups_layers()
        self.plot_quench_prop_and_resist()
        self.plot_half_turns()
        self.plot_electrical_order()
        self.plot_heat_exchange_order()
        self.plot_nonlin_induct()
        self.plot_psu_and_trig()
        self.plot_power_supl_contr()
