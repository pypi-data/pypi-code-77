# This file is part of PyEMMA.
#
# Copyright (c) 2016-2017 Computational Molecular Biology Group, Freie Universitaet Berlin (GER)
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
import warnings as _warnings

from pyemma._base.estimator import Estimator as _Estimator
from pyemma._base.progress import ProgressReporter as _ProgressReporter
from pyemma.thermo import MEMM as _MEMM
from pyemma.thermo.estimators._base import ThermoBase
from pyemma.thermo.models.memm import ThermoMSM as _ThermoMSM
from pyemma.util import types as _types
from pyemma.thermo.estimators._callback import _ConvergenceProgressIndicatorCallBack
from pyemma.thermo.estimators._callback import _IterationProgressIndicatorCallBack


from pyemma.thermo.extensions import (
    tram as _tram,
    tram_direct as _tram_direct,
    trammbar as _trammbar,
    trammbar_direct as _trammbar_direct,
    mbar as _mbar,
    mbar_direct as _mbar_direct,
    util as _util,
    cset as _cset,
)

from msmtools.estimation import largest_connected_set as _largest_connected_set


class EmptyState(RuntimeWarning):
    pass


class TRAM(_Estimator, _MEMM, ThermoBase):
    r"""Transition(-based) Reweighting Analysis Method."""
    __serialize_version = 0
    __serialize_fields = ('biased_conf_energies',
                          'btrajs',
                          'count_matrices',
                          'csets',
                          'dtrajs',
                          'equilibrium_btrajs',
                          'equilibrium_dtrajs',
                          'equilibrium_state_counts',
                          'equilibrium_state_counts_full',
                          'increments',
                          'log_lagrangian_mult',
                          'loglikelihoods',
                          'mbar_biased_conf_energies',
                          'mbar_therm_energies',
                          'mbar_unbiased_conf_energies',
                          'nthermo',
                          'state_counts',
                          'therm_energies',
                          'therm_state_counts_full',
                          )

    def __init__(
        self, lag, count_mode='sliding',
        connectivity='post_hoc_RE',
        nstates_full=None, equilibrium=None,
        maxiter=10000, maxerr=1.0E-15, save_convergence_info=0, dt_traj='1 step',
        nn=None, connectivity_factor=1.0, direct_space=False, N_dtram_accelerations=0,
        callback=None,
        init='mbar', init_maxiter=5000, init_maxerr=1.0E-8,
        overcounting_factor=1.0):
        r"""Transition(-based) Reweighting Analysis Method

        Parameters
        ----------
        lag : int
            Integer lag time at which transitions are counted.
        count_mode : str, optional, default='sliding'
            mode to obtain count matrices from discrete trajectories. Should be
            one of:
            * 'sliding' : A trajectory of length T will have :math:`T-\tau` counts at time indexes
                  .. math::
                     (0 \rightarrow \tau), (1 \rightarrow \tau+1), ..., (T-\tau-1 \rightarrow T-1)
            * 'sample' : A trajectory of length T will have :math:`T/\tau` counts
              at time indexes
                  .. math::
                        (0 \rightarrow \tau), (\tau \rightarrow 2 \tau), ..., ((T/\tau-1) \tau \rightarrow T)
            Currently only 'sliding' is supported.
        connectivity : str, optional, default='post_hoc_RE'
            One of 'post_hoc_RE', 'BAR_variance', 'reversible_pathways' or
            'summed_count_matrix'. Defines what should be considered a connected set
            in the joint (product) space of conformations and thermodynamic ensembles.
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
            * 'post_hoc_RE' : similar to 'reversible_pathways' but with a more strict
              requirement for the overlap between thermodynamic states. It is required
              that every state in the connected set can be reached by following a
              pathway of reversible transitions or jumping between overlapping
              thermodynamic states while staying in the same Markov state. A reversible
              transition between two Markov states (within the same thermodynamic
              state k) is a pair of Markov states that belong to the same strongly
              connected component of the count matrix (from thermodynamic state k).
              Two thermodynamic states k and l are defined to overlap at Markov state
              n if a replica exchange simulation [2]_ restricted to state n would show
              at least one transition from k to l or one transition from from l to k.
              The expected number of replica exchanges is estimated from the
              simulation data. The minimal number required of replica exchanges
              per Markov state can be increased by decreasing `connectivity_factor`.
            * 'BAR_variance' : like 'post_hoc_RE' but with a different condition to
              define the thermodynamic overlap based on the variance of the BAR
              estimator [3]_. Two thermodynamic states k and l are defined to overlap
              at Markov state n if the variance of the free energy difference Delta
              f_{kl} computed with BAR (and restricted to conformations form Markov
              state n) is less or equal than one. The minimally required variance
              can be controlled with `connectivity_factor`.
            * 'summed_count_matrix' : all thermodynamic states are assumed to overlap.
              The connected set is then computed by summing the count matrices over
              all thermodynamic states and taking it's largest strongly connected set.
              Not recommended!
            For more details see :func:`pyemma.thermo.extensions.cset.compute_csets_TRAM`.
        nstates_full : int, optional, default=None
            Number of cluster centers, i.e., the size of the full set of states.
        equilibrium : list of booleans, optional
            For every trajectory triple (ttraj[i], dtraj[i], btraj[i]), indicates
            whether to assume global equilibrium. If true, the triple is not used
            for computing kinetic quantities (but only thermodynamic quantities).
            By default, no trajectory is assumed to be in global equilibrium.
            This is the TRAMMBAR extension.
        maxiter : int, optional, default=10000
            The maximum number of self-consistent iterations before the estimator exits unsuccessfully.
        maxerr : float, optional, default=1E-15
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
        connectivity_factor : float, optional, default=1.0
            Only needed if connectivity='post_hoc_RE' or 'BAR_variance'. Values
            greater than 1.0 weaken the connectivity conditions. For 'post_hoc_RE'
            this multiplies the number of hypothetically observed transitions. For
            'BAR_variance' this scales the threshold for the minimal allowed variance
            of free energy differences.
        direct_space : bool, optional, default=False
            Whether to perform the self-consistent iteration with Boltzmann factors
            (direct space) or free energies (log-space). When analyzing data from
            multi-temperature simulations, direct-space is not recommended.
        N_dtram_accelerations : int, optional, default=0
            Convergence of TRAM can be speeded up by interleaving the updates
            in the self-consistent iteration with a dTRAM-like update step.
            N_dtram_accelerations says how many times the dTRAM-like update
            step should be applied in every iteration of the TRAM equations.
            Currently this is only effective if direct_space=True.
        init : str, optional, default=None
            Use a specific initialization for self-consistent iteration:

            | None:    use a hard-coded guess for free energies and Lagrangian multipliers
            | 'mbar':  perform a short MBAR estimate to initialize the free energies
        init_maxiter : int, optional, default=5000
            The maximum number of self-consistent iterations during the initialization.
        init_maxerr : float, optional, default=1.0E-8
            Convergence criterion for the initialization.
        overcounting_factor : double, default = 1.0
            Only needed if equilibrium contains True (TRAMMBAR).
            Sets the relative statistical weight of equilibrium and non-equilibrium
            frames. An overcounting_factor of value n means that every
            non-equilibrium frame is counted n times. Values larger than 1 increase
            the relative weight of the non-equilibrium data. Values less than 1
            increase the relative weight of the equilibrium data.


        References
        ----------
        .. [1] Wu, H. et al 2016
            Multiensemble Markov models of molecular thermodynamics and kinetics
            Proc. Natl. Acad. Sci. USA 113 E3221--E3230
        .. [2]_ Hukushima et al, Exchange Monte Carlo method and application to spin
            glass simulations, J. Phys. Soc. Jan. 65, 1604 (1996)
        .. [3]_ Shirts and Chodera, Statistically optimal analysis of samples
            from multiple equilibrium states, J. Chem. Phys. 129, 124105 (2008)

        """
        self.lag = lag
        assert count_mode == 'sliding', 'Currently the only implemented count_mode is \'sliding\''
        self.count_mode = count_mode
        self.connectivity = connectivity
        self.nn = nn
        self.connectivity_factor = connectivity_factor
        self.dt_traj = dt_traj
        self.nstates_full = nstates_full
        self.equilibrium = equilibrium
        self.maxiter = maxiter
        self.maxerr = maxerr
        self.direct_space = direct_space
        self.N_dtram_accelerations = N_dtram_accelerations
        self.callback = callback
        self.save_convergence_info = save_convergence_info
        assert init in (None, 'mbar'), 'Currently only None and \'mbar\' are supported'
        self.init = init
        self.init_maxiter = init_maxiter
        self.init_maxerr = init_maxerr
        self.overcounting_factor = overcounting_factor
        self.active_set = None
        self.biased_conf_energies = None
        self.mbar_therm_energies = None
        self.log_lagrangian_mult = None
        self.loglikelihoods = None

    def estimate(self, X, **params):
        """
        Parameters
        ----------
        X : tuple of (ttrajs, dtrajs, btrajs)
            Simulation trajectories. ttrajs contain the indices of the thermodynamic state, dtrajs
            contains the indices of the configurational states and btrajs contain the biases.

            ttrajs : list of numpy.ndarray(X_i, dtype=int)
                Every element is a trajectory (time series). ttrajs[i][t] is the index of the
                thermodynamic state visited in trajectory i at time step t.
            dtrajs : list of numpy.ndarray(X_i, dtype=int)
                dtrajs[i][t] is the index of the configurational state (Markov state) visited in
                trajectory i at time step t.
            btrajs : list of numpy.ndarray((X_i, T), dtype=numpy.float64)
                For every simulation frame seen in trajectory i and time step t, btrajs[i][t,k] is the
                bias energy of that frame evaluated in the k'th thermodynamic state (i.e. at the k'th
                Umbrella/Hamiltonian/temperature).
        """
        return super(TRAM, self).estimate(X, **params)

    def _estimate(self, X):
        ttrajs, dtrajs_full, btrajs = X
        # shape and type checks
        assert len(ttrajs) == len(dtrajs_full) == len(btrajs)
        for t in ttrajs:
            _types.assert_array(t, ndim=1, kind='i')
        for d in dtrajs_full:
            _types.assert_array(d, ndim=1, kind='i')
        for b in btrajs:
            _types.assert_array(b, ndim=2, kind='f')
        # find dimensions
        nstates_full = max(_np.max(d) for d in dtrajs_full) + 1
        if self.nstates_full is None:
            self.nstates_full = nstates_full
        elif self.nstates_full < nstates_full:
            raise RuntimeError("Found more states (%d) than specified by nstates_full (%d)" % (
                nstates_full, self.nstates_full))
        self.nthermo = max(_np.max(t) for t in ttrajs) + 1
        # dimensionality checks
        for t, d, b, in zip(ttrajs, dtrajs_full, btrajs):
            assert t.shape[0] == d.shape[0] == b.shape[0]
            assert b.shape[1] == self.nthermo

        # cast types and change axis order if needed
        ttrajs = [_np.require(t, dtype=_np.intc, requirements='C') for t in ttrajs]
        dtrajs_full = [_np.require(d, dtype=_np.intc, requirements='C') for d in dtrajs_full]
        btrajs = [_np.require(b, dtype=_np.float64, requirements='C') for b in btrajs]

        # if equilibrium information is given, separate the trajectories
        if self.equilibrium is not None:
            assert len(self.equilibrium) == len(ttrajs)
            _ttrajs, _dtrajs_full, _btrajs = ttrajs, dtrajs_full, btrajs
            ttrajs = [ttraj for eq, ttraj in zip(self.equilibrium, _ttrajs) if not eq]
            dtrajs_full = [dtraj for eq, dtraj in zip(self.equilibrium, _dtrajs_full) if not eq]
            self.btrajs = [btraj for eq, btraj in zip(self.equilibrium, _btrajs) if not eq]
            equilibrium_ttrajs = [ttraj for eq, ttraj in zip(self.equilibrium, _ttrajs) if eq]
            equilibrium_dtrajs_full = [dtraj for eq, dtraj in zip(self.equilibrium, _dtrajs_full) if eq]
            self.equilibrium_btrajs = [btraj for eq, btraj in zip(self.equilibrium, _btrajs) if eq]
        else: # set dummy values
            equilibrium_ttrajs = []
            equilibrium_dtrajs_full = []
            self.equilibrium_btrajs = []
            self.btrajs = btrajs

        # find state visits and transition counts
        state_counts_full = _util.state_counts(ttrajs, dtrajs_full, nstates=self.nstates_full, nthermo=self.nthermo)
        count_matrices_full = _util.count_matrices(ttrajs, dtrajs_full,
            self.lag, sliding=self.count_mode, sparse_return=False, nstates=self.nstates_full, nthermo=self.nthermo)
        self.therm_state_counts_full = state_counts_full.sum(axis=1)

        if self.equilibrium is not None:
            self.equilibrium_state_counts_full = _util.state_counts(equilibrium_ttrajs, equilibrium_dtrajs_full,
                nstates=self.nstates_full, nthermo=self.nthermo)
        else:
            self.equilibrium_state_counts_full = _np.zeros((self.nthermo, self.nstates_full), dtype=_np.float64)

        pg = _ProgressReporter()
        stage = 'cset'
        with pg.context(stage=stage):
            self.csets, pcset = _cset.compute_csets_TRAM(
                self.connectivity, state_counts_full, count_matrices_full,
                equilibrium_state_counts=self.equilibrium_state_counts_full,
                ttrajs=ttrajs+equilibrium_ttrajs, dtrajs=dtrajs_full+equilibrium_dtrajs_full, bias_trajs=self.btrajs+self.equilibrium_btrajs,
                nn=self.nn, factor=self.connectivity_factor,
                callback=_IterationProgressIndicatorCallBack(pg, 'finding connected set', stage=stage))
            self.active_set = pcset

        # check for empty states
        for k in range(self.nthermo):
            if len(self.csets[k]) == 0:
                _warnings.warn(
                    'Thermodynamic state %d' % k \
                    + ' contains no samples after reducing to the connected set.', EmptyState)

        # deactivate samples not in the csets, states are *not* relabeled
        self.state_counts, self.count_matrices, self.dtrajs, _  = _cset.restrict_to_csets(
            self.csets,
            state_counts=state_counts_full, count_matrices=count_matrices_full,
            ttrajs=ttrajs, dtrajs=dtrajs_full)

        if self.equilibrium is not None:
            self.equilibrium_state_counts, _, self.equilibrium_dtrajs, _ =  _cset.restrict_to_csets(
                self.csets,
                state_counts=self.equilibrium_state_counts_full, ttrajs=equilibrium_ttrajs, dtrajs=equilibrium_dtrajs_full)
        else:
            self.equilibrium_state_counts = _np.zeros((self.nthermo, self.nstates_full), dtype=_np.intc) # (remember: no relabeling)
            self.equilibrium_dtrajs = []

        # self-consistency tests
        assert _np.all(self.state_counts >= _np.maximum(self.count_matrices.sum(axis=1), \
            self.count_matrices.sum(axis=2)))
        assert _np.all(_np.sum(
            [_np.bincount(d[d>=0], minlength=self.nstates_full) for d in self.dtrajs],
            axis=0) == self.state_counts.sum(axis=0))
        assert _np.all(_np.sum(
            [_np.bincount(t[d>=0], minlength=self.nthermo) for t, d in zip(ttrajs, self.dtrajs)],
            axis=0) == self.state_counts.sum(axis=1))
        if self.equilibrium is not None:
            assert _np.all(_np.sum(
                [_np.bincount(d[d >= 0], minlength=self.nstates_full) for d in self.equilibrium_dtrajs],
                axis=0) == self.equilibrium_state_counts.sum(axis=0))
            assert _np.all(_np.sum(
                [_np.bincount(t[d >= 0], minlength=self.nthermo) for t, d in zip(equilibrium_ttrajs, self.equilibrium_dtrajs)],
                axis=0) ==  self.equilibrium_state_counts.sum(axis=1))

        # check for empty states
        for k in range(self.state_counts.shape[0]):
            if self.count_matrices[k, :, :].sum() == 0 and self.equilibrium_state_counts[k, :].sum()==0:
                _warnings.warn(
                    'Thermodynamic state %d' % k \
                    + ' contains no transitions and no equilibrium data after reducing to the connected set.', EmptyState)

        if self.init == 'mbar' and self.biased_conf_energies is None:
            if self.direct_space:
                mbar = _mbar_direct
            else:
                mbar = _mbar
            stage = 'MBAR init.'
            with pg.context(stage=stage):
                self.mbar_therm_energies, self.mbar_unbiased_conf_energies, \
                    self.mbar_biased_conf_energies, _ = mbar.estimate(
                        (state_counts_full.sum(axis=1)+self.equilibrium_state_counts_full.sum(axis=1)).astype(_np.intc),
                        self.btrajs+self.equilibrium_btrajs, dtrajs_full+equilibrium_dtrajs_full,
                        maxiter=self.init_maxiter, maxerr=self.init_maxerr,
                        callback=_ConvergenceProgressIndicatorCallBack(
                            pg, stage, self.init_maxiter, self.init_maxerr),
                        n_conf_states=self.nstates_full)
            self.biased_conf_energies = self.mbar_biased_conf_energies.copy()

        # run estimator
        if self.direct_space:
            tram = _tram_direct
            trammbar = _trammbar_direct
        else:
            tram = _tram
            trammbar = _trammbar
        #import warnings
        #with warnings.catch_warnings() as cm:
        # warnings.filterwarnings('ignore', RuntimeWarning)
        stage = 'TRAM'
        with pg.context(stage=stage):
            if self.equilibrium is None:
                self.biased_conf_energies, conf_energies, self.therm_energies, self.log_lagrangian_mult, \
                    self.increments, self.loglikelihoods = tram.estimate(
                        self.count_matrices, self.state_counts, self.btrajs, self.dtrajs,
                        maxiter=self.maxiter, maxerr=self.maxerr,
                        biased_conf_energies=self.biased_conf_energies,
                        log_lagrangian_mult=self.log_lagrangian_mult,
                        save_convergence_info=self.save_convergence_info,
                        callback=_ConvergenceProgressIndicatorCallBack(
                            pg, stage, self.maxiter, self.maxerr, subcallback=self.callback),
                        N_dtram_accelerations=self.N_dtram_accelerations)
            else: # use trammbar
                self.biased_conf_energies, conf_energies, self.therm_energies, self.log_lagrangian_mult, \
                    self.increments, self.loglikelihoods = trammbar.estimate(
                        self.count_matrices, self.state_counts, self.btrajs, self.dtrajs,
                        equilibrium_therm_state_counts=self.equilibrium_state_counts.sum(axis=1).astype(_np.intc),
                        equilibrium_bias_energy_sequences=self.equilibrium_btrajs, equilibrium_state_sequences=self.equilibrium_dtrajs,
                        maxiter=self.maxiter, maxerr=self.maxerr,
                        save_convergence_info=self.save_convergence_info,
                        biased_conf_energies=self.biased_conf_energies,
                        log_lagrangian_mult=self.log_lagrangian_mult,
                        callback=_ConvergenceProgressIndicatorCallBack(
                            pg, stage, self.maxiter, self.maxerr, subcallback=self.callback),
                        N_dtram_accelerations=self.N_dtram_accelerations,
                        overcounting_factor=self.overcounting_factor)

        # compute models
        fmsms = [_np.ascontiguousarray((
            _tram.estimate_transition_matrix(
                self.log_lagrangian_mult, self.biased_conf_energies, self.count_matrices, None,
                K)[self.active_set, :])[:, self.active_set]) for K in range(self.nthermo)]

        active_sets = [_largest_connected_set(msm, directed=False) for msm in fmsms]
        fmsms = [_np.ascontiguousarray(
            (msm[lcc, :])[:, lcc]) for msm, lcc in zip(fmsms, active_sets)]

        models = []
        for i, (msm, acs) in enumerate(zip(fmsms, active_sets)):
            pi_acs = _np.exp(self.therm_energies[i] - self.biased_conf_energies[i, :])[self.active_set[acs]]
            pi_acs = pi_acs / pi_acs.sum()
            models.append(_ThermoMSM(
                msm, self.active_set[acs], self.nstates_full, pi=pi_acs,
                dt_model=self.timestep_traj.get_scaled(self.lag)))

        # set model parameters to self
        self.set_model_params(
            models=models, f_therm=self.therm_energies, f=conf_energies[self.active_set].copy())

        return self

    def log_likelihood(self):
        r"""
        Returns the value of the log-likelihood of the converged TRAM estimate.
        """
        # TODO: check that we are estimated...
        return _tram.log_likelihood_lower_bound(
            self.log_lagrangian_mult, self.biased_conf_energies,
            self.count_matrices, self.btrajs, self.dtrajs, self.state_counts,
            None, None, None, None, None)

    def pointwise_free_energies(self, therm_state=None):
        r"""
        Computes the pointwise free energies :math:`-\log(\mu^k(x))` for all points x.

        :math:`\mu^k(x)` is the optimal estimate of the Boltzmann distribution
        of the k'th ensemble defined on the set of all samples.

        Parameters
        ----------
        therm_state : int or None, default=None
            Selects the thermodynamic state k for which to compute the
            pointwise free energies.
            None selects the "unbiased" state which is defined by having
            zero bias energy.

        Returns
        -------
        mu_k : list of numpy.ndarray(X_i, dtype=numpy.float64)
             list of the same layout as dtrajs (or ttrajs). mu_k[i][t]
             contains the pointwise free energy of the frame seen in
             trajectory i and time step t.
             Frames that are not in the connected sets get assiged an
             infinite pointwise free energy.
        """
        assert self.therm_energies is not None, \
            'MEMM has to be estimate()\'d before pointwise free energies can be calculated.'
        if therm_state is not None:
            assert therm_state<=self.nthermo
        mu = [_np.zeros(d.shape[0], dtype=_np.float64) for d in self.dtrajs+self.equilibrium_dtrajs]
        if self.equilibrium is None:
            _tram.get_pointwise_unbiased_free_energies(
                therm_state,
                self.log_lagrangian_mult, self.biased_conf_energies,
                self.therm_energies, self.count_matrices,
                self.btrajs, self.dtrajs,
                self.state_counts, None, None, mu)
        else:
            _trammbar.get_pointwise_unbiased_free_energies(
                therm_state,
                self.log_lagrangian_mult, self.biased_conf_energies,
                self.therm_energies, self.count_matrices,
                self.btrajs+self.equilibrium_btrajs, self.dtrajs+self.equilibrium_dtrajs,
                self.state_counts, None, None, mu,
                equilibrium_therm_state_counts=self.equilibrium_state_counts.sum(axis=1).astype(_np.intc),
                overcounting_factor=1.0/self.lag)
        return mu

    def mbar_pointwise_free_energies(self, therm_state=None):
        assert self.mbar_therm_energies is not None, \
            'MEMM has to be estimate()\'d with init=\'mbar\' before pointwise free energies can be calculated.'
        if therm_state is not None:
            assert therm_state<=self.nthermo
        mu = [_np.zeros(d.shape[0], dtype=_np.float64) for d in self.dtrajs+self.equilibrium_dtrajs]
        _mbar.get_pointwise_unbiased_free_energies(therm_state,
            _np.log(self.therm_state_counts_full + self.equilibrium_state_counts_full.sum(axis=1)).astype(_np.float64),
            self.btrajs+self.equilibrium_btrajs, self.mbar_therm_energies, None, mu)
        return mu

    def __getstate__(self):
        # do not pickle callable
        state = super(TRAM, self).__getstate__()
        state.pop('callback', None)
        return state
