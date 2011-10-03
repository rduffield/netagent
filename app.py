#!/usr/bin/env python

import datetime
import json
import sys
import time
from stats import ProcNetNetstat

class App(object):
    """Main app"""
    def __init__(self):
        super(App, self).__init__()
        if sys.platform == 'darwin':
            self.stats = ProcNetNetstat('tests/netstat')
        else:
            self.stats = ProcNetNetstat()

    def run(self):
        while True:
            data = self.stats.run()
            data['Date'] = time.mktime(datetime.datetime.utcnow().timetuple())
            print json.dumps(data)
            time.sleep(10)

if __name__ == '__main__':
    app = App()
    app.run()
