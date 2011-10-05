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
    usage = 'usage: %prog [options]'
    parser = OptionParser(usage=usage)
    parser.add_option('-k', '--key', dest='key', help='key to collect data for e.g. TcpExt')
    (options, args) = parser.parse_args()

    if options.key:
        app = App(options.key)
        app.run()
    else:
        parser.error('incorrect number of arguments')
        sys.exit(1)

        