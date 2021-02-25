from optimeed.core import LinkDataGraph, HowToPlotGraph
from optimeed.visualize.gui.widgets.widget_graphs_visual import widget_graphs_visual
from optimeed.visualize.gui.gui_mainWindow import gui_mainWindow
from optimeed.visualize.gui.widgets.graphsVisualWidget.smallGui import guiPyqtgraph
from optimeed.core import ListDataStruct, Performance_ListDataStruct
from optimeed.core import Graphs
import os


class _OptiProjectLoader:
    """A loader for an opti project."""
    def __init__(self, foldername, kwargsPlot=None):
        """

        :param foldername: the folder containing the saved files.
        :param kwargsPlot: Check kgwargs `~optimeed.core.graphs.Data`
        """
        self.logopti = ListDataStruct.load(os.path.join(foldername, "logopti.json"))
        self.theDevices = Performance_ListDataStruct.load(os.path.join(foldername, "autosaved.json"))
        self.theConvergence = ListDataStruct.load(os.path.join(foldername, "optiConvergence.json"))
        self.kwargsPlot = kwargsPlot

    def get_devices(self):
        return self.theDevices

    def get_logopti(self):
        return self.logopti

    def get_convergence(self):
        return self.theConvergence.get_data_at_index(0)

    def get_kwargs(self):
        return dict() if self.kwargsPlot is None else self.kwargsPlot

    def get_nbr_objectives(self):
        return len(self.logopti.get_data_at_index(0).objectives)


class ViewOptimizationResults:
    """Convenience class to display the results of an optimization"""

    def __init__(self):
        self.optiProjects = list()
        self.theDataLink = LinkDataGraph()

    def add_opti_project(self, foldername, kwargsPlot=None):
        """Add an opti project to visualize.

        :param foldername: the folder containing the saved files. (as string)
        :param kwargsPlot: Check kgwargs `~optimeed.core.graphs.Data`
        """
        self.optiProjects.append(_OptiProjectLoader(foldername, kwargsPlot))

    def get_data_link(self) -> LinkDataGraph:
        """Return the object :class:`~optimeed.core.linkDataGraph.LinkDataGraph`"""
        return self.theDataLink

    def display_graphs(self, theActionsOnClick=None, kwargs_common=None, keep_alive=True):
        """Generates the optimization graphs.

        :param theActionsOnClick: list of actions to perform when a graph is clicked
        :param kwargs_common: plot options (from Data class) to apply to all the graphs (ex: {"is_scattered": True}).
        :param keep_alive: if set to true, this method will be blocking. Otherwise you should manually call start_qt_mainloop().
        :return: widget_graphs_visual for the log opti, widget_graphs_visual for the convergence (:class:`~widget_graphs_visual`)
        """
        if theActionsOnClick is None:
            theActionsOnClick = list()

        nbrObjectives = self.optiProjects[0].get_nbr_objectives()
        theDataLink = self.theDataLink

        # Creates empty graphs
        listOf_howtoplot = list()

        base_kwargs = {'is_scattered': True}
        if kwargs_common is not None:
            base_kwargs.update(kwargs_common)

        if nbrObjectives == 2:  # bi-objective -> each objective is an axis
            howToPlot = HowToPlotGraph('objectives[0]', 'objectives[1]', base_kwargs)
            theDataLink.add_graph(howToPlot)  # Creates a graph
            listOf_howtoplot.append(howToPlot)
        elif nbrObjectives == 3:  # 3-objectives -> plot graphs by pairs of objective
            for i in range(nbrObjectives):
                i_plus_1 = i + 1 if i is not 2 else 2
                curr_i = i if i is not 2 else 0
                howToPlot = HowToPlotGraph('objectives[{}]'.format(curr_i), 'objectives[{}]'.format(i_plus_1), base_kwargs)
                theDataLink.add_graph(howToPlot)  # Creates a graph
                listOf_howtoplot.append(howToPlot)
        else:  # Plot each objective as a function of the time
            for i in range(nbrObjectives):
                howToPlot = HowToPlotGraph(None, 'objectives[{}]'.format(i), base_kwargs)
                theDataLink.add_graph(howToPlot)  # Creates a graph
                listOf_howtoplot.append(howToPlot)

        # Graphs are created, now add the data to it.
        listOf_idLogopti = list()
        for theOptiProject in self.optiProjects:
            collection_devices = theOptiProject.get_devices()
            collection_logOpti = theOptiProject.get_logopti()

            id_logOpti = theDataLink.add_collection(collection_logOpti, kwargs=theOptiProject.get_kwargs())
            id_devices = theDataLink.add_collection(collection_devices)

            listOf_idLogopti.append(id_logOpti)

            """The trick here is that the objective functions is not directly stocked in collection_devices but in collection_logOpti. 
            So we display the objectives coming from collection_logOpti but we link collection_devices from it.
            So that when a point is clicked, the action is performed on the device and not on the logOpti."""
            theDataLink.link_collection_to_graph_collection(id_logOpti, id_devices)
            for howtoplot in listOf_howtoplot:
                howtoplot.exclude_col(id_devices)

        """Generate the graphs (without displaying them yet)"""
        theGraphs = theDataLink.createGraphs()

        """Create the widget of the graphs, and the associated GUI"""
        myWidgetGraphsVisuals = widget_graphs_visual(theGraphs, highlight_last=True, refresh_time=-1)
        guiPyqtgraph(myWidgetGraphsVisuals, actionsOnClick=theActionsOnClick)  # Add GUI to change action easily and export graphs

        """Manipulates the graphs to change the appearance of points violating the constraints"""
        def __change_appearance_violate_constraints():
            for _id_logOpti in listOf_idLogopti:
                graphs, theCol = theDataLink.get_graph_and_trace_from_collection(_id_logOpti)
                all_constraints = theCol.get_list_attributes("constraints")
                violate_constraint_indices = list()
                for index, constraints in enumerate(all_constraints):
                    for constraint in constraints:
                        if constraint > 0:
                            violate_constraint_indices.append(index)  # Index in data
                for graph, trace in graphs:
                    theTrace = myWidgetGraphsVisuals.get_graph(graph).get_trace(trace)
                    theTrace.set_brushes(violate_constraint_indices, (250, 0, 0))

        __change_appearance_violate_constraints()

        """Spawn the GUI"""
        theWindow = gui_mainWindow([myWidgetGraphsVisuals])
        theWindow.run(hold=False)

        """Spawn an other GUI for the convergence graphs"""
        graphs_convergence = Graphs()
        for theOptiProject in self.optiProjects:
            newGraphs = theOptiProject.get_convergence().get_graphs()
            newGraphs.get_first_graph().get_trace(0).set_legend(theOptiProject.get_kwargs().get("legend", ''))
            graphs_convergence.merge(newGraphs)
        wg_graphs_convergence = widget_graphs_visual(graphs_convergence, highlight_last=False, refresh_time=-1)
        guiPyqtgraph(wg_graphs_convergence)  # Add GUI to change action easily and export graphs

        myWindow = gui_mainWindow([wg_graphs_convergence])
        myWindow.run(hold=keep_alive)

        return myWidgetGraphsVisuals, wg_graphs_convergence
