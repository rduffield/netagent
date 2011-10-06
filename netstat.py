#!/usr/bin/env python

import sys
import json
import time
from optparse import OptionParser
from stats import ProcNetNetstat

class App(object):
    def __init__(self, key):
        super(App, self).__init__()
        self.key = key
        if sys.platform == 'darwin':
            self.stats = ProcNetNetstat('tests/netstat', key=key)
        else:
            self.stats = ProcNetNetstat(key=key)

    def run(self):
        while True:
            stats = self.stats.run()
            sys.stdout.write(json.dumps(stats))
            sys.stdout.write('\n')
            sys.stdout.flush()
            time.sleep(5)

if __name__ == '__main__':
    usage = 'usage: %prog key'
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()

    if len(args) == 1:
        app = App(args[0])
        app.run()
    else:
        parser.error('incorrect number of arguments')
        sys.exit(1)

        