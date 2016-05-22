# -*- coding:utf8 -*-
"""Bot class extensions
"""
import datetime
from errcron import cronjob


class CrontabMixin(object):
    """Mix-in class to implement crontab features

    If you will use crontab by it, call activate_crontab
    """
    def activate_crontab(self):
        """Activate polling function and register first crontab
        """
        self._crontab = []
        if hasattr(self, 'CRONTAB'):
            for crontab_spec in self.CRONTAB:
                job = cronjob.load_from_string(crontab_spec)
                self._crontab.append(job)

    def poll_crontab(self):
        """Check crontab and run target jobs
        """
        polled_time = datetime.datetime.now()
        for cronjob in self._crontab:
            if not cronjob.is_runnable(polled_time):
                continue
            cronjob.action(self, polled_time)
