#!/usr/bin/env python

import time
from stats import ProcNetNetstat

class App(object):
    """Main app"""
    def __init__(self):
        super(App, self).__init__()
        self.stats = ProcNetNetstat()

    def run(self):
        while True:
            self.stats.run()
            time.sleep(5)

if __name__ == '__main__':
    app = App()
    app.run()
