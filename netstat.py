#!/usr/bin/env python

import datetime
import json
import sys
import time
from optparse import OptionParser
from stats import ProcNetNetstat

class Netstat(object):
    def __init__(self):
        super(Netstat, self).__init__()
        if sys.platform == 'darwin':
            self.stats = ProcNetNetstat('tests/netstat')
        else:
            self.stats = ProcNetNetstat()

    def run(self):
        while True:
            stats = self.stats.run()
            stats['Date'] = time.mktime(datetime.datetime.utcnow().timetuple())
            sys.stdout.write(json.dumps(stats))
            sys.stdout.write('\n')
            sys.stdout.flush()
            time.sleep(5)

if __name__ == '__main__':
    usage = 'usage: %prog key'
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    netstat = Netstat()
    netstat.run()

        