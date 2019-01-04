#!/usr/bin/env python
# -*- coding: utf-8 -*-\

import datetime
from system.Logger import Logger
from system.Helper import Helper
from system.Graphium import Graphium


class Analytics():

    _logger = None
    _helper = None
    _g = None

    _last_sync = None

    def __init__(self, logger=None):

        self._g = Graphium()
        self._helper = Helper()

        if logger is None:
            self._logger = Logger('MemoryStats')
        else:
            self._logger = logger

        self._last_sync = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    def memory_analises(self):
        date_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        if self._helper.get_time_elapsed(self._last_sync, date_now) < self._g.analytics['time_between_analises']:
            self._last_sync = date_now

            self._memory_summary()
        else:
            self._logger.info("Analytics: Waiting appropriate time...")

    def _memory_summary(self):

        # Only import Pympler when we need it. We don't want it to
        # affect our process if we never call memory_summary.
        from pympler import summary, muppy

        mem_summary = summary.summarize(muppy.get_objects())
        rows = summary.format_(mem_summary)
        stack_memory = '\n'.join(rows)

        self._logger.info("Analytics: Memory Analytic\n")
        self._logger.info(stack_memory)
