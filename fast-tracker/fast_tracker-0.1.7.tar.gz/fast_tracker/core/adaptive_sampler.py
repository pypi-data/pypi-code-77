# -*- coding: utf-8 -*-
import random
import time
import threading


class AdaptiveSampler(object):
    def __init__(self, sampling_target, sampling_period):
        """

        :param sampling_target:  采样点数
        :param sampling_period:  采样周期
        """
        self.adaptive_target = 0.0
        self.period = sampling_period
        self.last_reset = time.time()
        self._lock = threading.Lock()

        self.sampling_target = sampling_target
        self.max_sampled = sampling_target
        self.computed_count_last = sampling_target

        self.computed_count = 0
        self.sampled_count = 0

    def reset_if_required(self):
        time_since_last_reset = time.time() - self.last_reset
        cycles = time_since_last_reset // self.period
        if cycles:
            self._reset()

            if cycles > 1:
                self._reset()

    def compute_sampled(self):
        with self._lock:
            self.reset_if_required()
            if self.sampled_count >= self.max_sampled:
                return False

            elif self.sampled_count < self.sampling_target:
                sampled = random.randrange(
                        self.computed_count_last) < self.sampling_target
                if sampled:
                    self.sampled_count += 1
            else:
                sampled = random.randrange(
                        self.computed_count) < self.adaptive_target
                if sampled:
                    self.sampled_count += 1

                    ratio = float(self.sampling_target) / self.sampled_count
                    self.adaptive_target = (self.sampling_target ** ratio -
                                            self.sampling_target ** 0.5)

            self.computed_count += 1
        return sampled

    def _reset(self):
        self.last_reset = time.time()
        self.max_sampled = 2 * self.sampling_target
        self.adaptive_target = (self.sampling_target -
                                self.sampling_target ** 0.5)

        self.computed_count_last = max(self.computed_count,
                                       self.sampling_target)
        self.computed_count = 0
        self.sampled_count = 0
