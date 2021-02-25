# This file is part of PyEMMA.
#
# Copyright (c) 2015-2017 Computational Molecular Biology Group, Freie Universitaet Berlin (GER)
#
# PyEMMA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as _np

from pyemma._base.estimator import Estimator as _Estimator
from pyemma._base.progress import ProgressReporter as _ProgressReporter
from pyemma.thermo import MEMM as _MEMM
from pyemma.thermo.estimators._base import ThermoBase
from pyemma.thermo.models.memm import ThermoMSM as _ThermoMSM
from pyemma.util import types as _types
from pyemma.thermo.estimators._callback import _ConvergenceProgressIndicatorCallBack

from msmtools.estimation import largest_connected_set as _largest_connected_set

from pyemma.thermo.extensions import (
    dtram as _dtram,
    wham as _wham,
    util as _util,
    cset as _cset
)

__author__ = 'noe, wehmeyer'


class DTRAM(_Estimator, _MEMM, ThermoBase):
    r""" Discrete Transition(-based) Reweighting Analysis Method."""
    __serialize_version = 0
    __serialize_fields = ('bias_energies',
                          'conf_energies',
                          'count_matrices',
                          'count_matrices_full',
                          'increments',
                          'log_lagrangian_mult',
                          'loglikelihoods',
                          'nthermo',
                          'state_counts',
                          'state_counts_full',
                          'therm_energies',
                          )

    def __init__(
        self, bias_energies_full, lag, count_mode='sliding', connectivity='reversible_pathways',
        maxiter=10000, maxerr=1.0E-15, save_convergence_info=0, dt_traj='1 step',
        init=None, init_maxiter=10000, init_maxerr=1.0E-8):
        r""" Discrete Transition(-based) Reweighting Analysis Method

        Parameters
        ----------
        bias_energies_full : numpy.ndarray(shape=(num_therm_states, num_conf_states)) object
            bias_energies_full[j, i] is the bias energy in units of kT for each discrete state i
            at thermodynamic state j.
        lag : int
            Integer lag time at which transitions are counted.
        count_mode : str, optional, default='sliding'
            Mode to obtain count matrices from discrete trajectories. Should be one of:
            * 'sliding' : a trajectory of length T will have :math:`T-\tau` counts at time indexes
                  .. math::
                     (0 \rightarrow \tau), (1 \rightarrow \tau+1), ..., (T-\tau-1 \rightarrow T-1)
            * 'sample' : a trajectory of length T will have :math:`T/\tau` counts at time indexes
                  .. math::
                        (0 \rightarrow \tau), (\tau \rightarrow 2 \tau), ..., ((T/\tau-1) \tau \rightarrow T)
            Currently only 'sliding' is supported.
        connectivity : str, optional, default='reversible_pathways'
            One of 'reversible_pathways', 'summed_count_matrix' or None.
            Defines what should be considered a connected set in the joint (product)
            space of conformations and thermodynamic ensembles.
            * 'reversible_pathways' : requires that every state in the connected set
              can be reached by following a pathway of reversible transitions. A
              reversible transition between two Markov states (within the same
              thermodynamic state k) is a pair of Markov states that belong to the
              same strongly connected component of the count matrix (from
              thermodynamic state k). A pathway of reversible transitions is a list of
              reversible transitions [(i_1, i_2), (i_2, i_3),..., (i_(N-2), i_(N-1)),
              (i_(N-1), i_N)]. The thermodynamic state where the reversible
              transitions happen, is ignored in constructing the reversible pathways.
              This is equivalent to assuming that two ensembles overlap at some Markov
              state whenever there exist frames from both ensembles in that Markov
              state.
            * 'summed_count_matrix' : all thermodynamic states are assumed to overlap.
              The connected set is then computed by summing the count matrices over
              all thermodynamic states and taking it's largest strongly connected set.
              Not recommended!
            * None : assume that everything is connected. For debugging.
            For more details see :func:`pyemma.thermo.extensions.cset.compute_csets_dTRAM`.
        maxiter : int, optional, default=10000
            The maximum number of self-consistent iterations before the estimator exits unsuccessfully.
        maxerr : float, optional, default=1.0E-15
            Convergence criterion based on the maximal free energy change in a self-consistent
            iteration step.
        save_convergence_info : int, optional, default=0
            Every save_convergence_info iteration steps, store the actual increment
            and the actual log-likelihood; 0 means no storage.
        dt_traj : str, optional, default='1 step'
            Description of the physical time corresponding to the lag. May be used by analysis
            algorithms such as plotting tools to pretty-print the axes. By default '1 step', i.e.
            there is no physical time unit.  Specify by a number, whitespace and unit. Permitted
            units are (* is an arbitrary string):

            |  'fs',   'femtosecond*'
            |  'ps',   'picosecond*'
            |  'ns',   'nanosecond*'
            |  'us',   'microsecond*'
            |  'ms',   'millisecond*'
            |  's',    'second*'
        init : str, optional, default=None
            Use a specific initialization for self-consistent iteration:

            | None:    use a hard-coded guess for free energies and Lagrangian multipliers
            | 'wham':  perform a short WHAM estimate to initialize the free energies
        init_maxiter : int, optional, default=10000
            The maximum number of self-consistent iterations during the initialization.
        init_maxerr : float, optional, default=1.0E-8
            Convergence criterion for the initialization.

        Example
        -------
        >>> from pyemma.thermo import DTRAM
        >>> import numpy as np
        >>> B = np.array([[0, 0],[0.5, 1.0]])
        >>> dtram = DTRAM(B, 1)
        >>> ttrajs = [np.array([0,0,0,0,0,0,0,0,0,0]),np.array([1,1,1,1,1,1,1,1,1,1])]
        >>> dtrajs = [np.array([0,0,0,0,1,1,1,0,0,0]),np.array([0,1,0,1,0,1,1,0,0,1])]
        >>> dtram = dtram.estimate((ttrajs, dtrajs))
        >>> dtram.log_likelihood() # doctest: +ELLIPSIS
        -9.805...
        >>> dtram.count_matrices # doctest: +SKIP
        array([[[5, 1],
                [1, 2]],

               [[1, 4],
                [3, 1]]], dtype=int32)
        >>> dtram.stationary_distribution # doctest: +ELLIPSIS
        array([ 0.38...,  0.61...])
        >>> dtram.meval('stationary_distribution') # doctest: +ELLIPSIS
        [array([ 0.38...,  0.61...]), array([ 0.50...,  0.49...])]

        References
        ----------

        .. [1] Wu, H. et al 2014
            Statistically optimal analysis of state-discretized trajectory data from multiple thermodynamic states
            J. Chem. Phys. 141, 214106

        """
        # set all parameters
        self.bias_energies_full = _types.ensure_ndarray(bias_energies_full, ndim=2, kind='numeric')
        self.lag = lag
        assert count_mode == 'sliding', 'Currently the only implemented count_mode is \'sliding\''
        self.count_mode = count_mode
        assert connectivity in [ None, 'reversible_pathways', 'summed_count_matrix' ], \
            'Currently the only implemented connectivity checks are \'reversible_pathways\', \'summed_count_matrix\' and None'
        self.connectivity = connectivity
        self.dt_traj = dt_traj
        self.maxiter = maxiter
        self.maxerr = maxerr
        self.save_convergence_info = save_convergence_info
        assert init in (None, 'wham'), 'Currently only None and \'wham\' are supported'
        self.init = init
        self.init_maxiter = init_maxiter
        self.init_maxerr = init_maxerr
        # set derived quantities
        self.nthermo, self.nstates_full = bias_energies_full.shape
        # set iteration variables
        self.therm_energies = None
        self.conf_energies = None
        self.log_lagrangian_mult = None

    def estimate(self, trajs):
        """
        Parameters
        ----------
        X : tuple of (ttrajs, dtrajs)
            Simulation trajectories. ttrajs contain the indices of the thermodynamic state and
            dtrajs contains the indices of the configurational states.

            ttrajs : list of numpy.ndarray(X_i, dtype=int)
                Every elements is a trajectory (time series). ttrajs[i][t] is the index of the
                thermodynamic state visited in trajectory i at time step t.
            dtrajs : list of numpy.ndarray(X_i, dtype=int)
                dtrajs[i][t] is the index of the configurational state (Markov state) visited in
                trajectory i at time step t.

        """
        return super(DTRAM, self).estimate(trajs)

    def _estimate(self, trajs):
        # check input
        assert isinstance(trajs, (tuple, list))
        assert len(trajs) == 2
        ttrajs = trajs[0]
        dtrajs = trajs[1]
        # validate input
        for ttraj, dtraj in zip(ttrajs, dtrajs):
            _types.assert_array(ttraj, ndim=1, kind='numeric')
            _types.assert_array(dtraj, ndim=1, kind='numeric')
            assert _np.shape(ttraj)[0] == _np.shape(dtraj)[0]

        # harvest transition counts
        self.count_matrices_full = _util.count_matrices(
            ttrajs, dtrajs, self.lag,
            sliding=self.count_mode, sparse_return=False, nstates=self.nstates_full)
        # harvest state counts (for WHAM)
        self.state_counts_full = _util.state_counts(
            ttrajs, dtrajs, nthermo=self.nthermo, nstates=self.nstates_full)

        # restrict to connected set
        C_sum = self.count_matrices_full.sum(axis=0)
        # TODO: use improved cset
        _, cset = _cset.compute_csets_dTRAM(self.connectivity, self.count_matrices_full)
        self.active_set = cset
        # correct counts
        self.count_matrices = self.count_matrices_full[:, cset[:, _np.newaxis], cset]
        self.count_matrices = _np.require(
            self.count_matrices, dtype=_np.intc ,requirements=['C', 'A'])
        # correct bias matrix
        self.bias_energies = self.bias_energies_full[:, cset]
        self.bias_energies = _np.require(
            self.bias_energies, dtype=_np.float64 ,requirements=['C', 'A'])
        # correct state counts
        self.state_counts = self.state_counts_full[:, cset]
        self.state_counts = _np.require(self.state_counts, dtype=_np.intc ,requirements=['C', 'A'])

        # run initialisation
        pg = _ProgressReporter()

        if self.init is not None and self.init == 'wham':
            stage = 'WHAM init.'
            with pg.context(stage=stage):
                self.therm_energies, self.conf_energies, _increments, _loglikelihoods = \
                    _wham.estimate(
                        self.state_counts, self.bias_energies,
                        maxiter=self.init_maxiter, maxerr=self.init_maxerr, save_convergence_info=0,
                        therm_energies=self.therm_energies, conf_energies=self.conf_energies,
                        callback=_ConvergenceProgressIndicatorCallBack(
                            pg, stage, self.init_maxiter, self.init_maxerr))

        # run estimator
        stage = 'DTRAM'
        with pg.context(stage=stage):
            self.therm_energies, self.conf_energies, self.log_lagrangian_mult, \
                self.increments, self.loglikelihoods = _dtram.estimate(
                    self.count_matrices, self.bias_energies,
                    maxiter=self.maxiter, maxerr=self.maxerr,
                    log_lagrangian_mult=self.log_lagrangian_mult,
                    conf_energies=self.conf_energies,
                    save_convergence_info=self.save_convergence_info,
                    callback=_ConvergenceProgressIndicatorCallBack(
                        pg, stage, self.maxiter, self.maxerr))

        # compute models
        fmsms = [_dtram.estimate_transition_matrix(
            self.log_lagrangian_mult, self.bias_energies, self.conf_energies,
            self.count_matrices, _np.zeros(
                shape=self.conf_energies.shape, dtype=_np.float64), K) for K in range(self.nthermo)]

        active_sets = [_largest_connected_set(msm, directed=False) for msm in fmsms]
        fmsms = [_np.ascontiguousarray(
            (msm[lcc, :])[:, lcc]) for msm, lcc in zip(fmsms, active_sets)]

        models = []
        for i, (msm, acs) in enumerate(zip(fmsms, active_sets)):
            pi_acs = _np.exp(self.therm_energies[i] - self.bias_energies[i, :] - self.conf_energies)[acs]
            pi_acs = pi_acs / pi_acs.sum()
            models.append(_ThermoMSM(
                msm, self.active_set[acs], self.nstates_full, pi=pi_acs,
                dt_model=self.timestep_traj.get_scaled(self.lag)))

        # set model parameters to self
        self.set_model_params(
            models=models, f_therm=self.therm_energies, f=self.conf_energies)

        # done
        return self

    def log_likelihood(self):
        return _dtram.get_loglikelihood(
            self.count_matrices,
            _dtram.estimate_transition_matrices(
                self.log_lagrangian_mult,
                self.bias_energies,
                self.conf_energies,
                self.count_matrices,
                _np.zeros(shape=self.conf_energies.shape, dtype=_np.float64)))
