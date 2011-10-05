#!/usr/bin/env python

import sys
import json
import time
from stats import ProcNetNetstat

class App(object):
    def __init__(self):
        super(App, self).__init__()
        if sys.platform == 'darwin':
            self.stats = ProcNetNetstat('tests/netstat')
        else:
            self.stats = ProcNetNetstat()

    def run(self):
        while True:
            stats = self.stats.run()
            sys.stdout.write(json.dumps(stats))
            sys.stdout.write('\n')
            sys.stdout.flush()
            time.sleep(5)

if __name__ == '__main__':
    app = App()
    app.run()

        