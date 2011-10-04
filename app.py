#!/usr/bin/env python

import datetime
import json
import requests
import sys
import time
from optparse import OptionParser
from stats import ProcNetNetstat

class App(object):
    def __init__(self, username, password, account, api_key, device_id, agent_key, api_host):
        super(App, self).__init__()

        self.username = username
        self.password = password
        self.account = account
        self.api_key = api_key
        self.device_id = device_id
        self.agent_key = agent_key
        self.api_host = api_host

        if sys.platform == 'darwin':
            self.stats = ProcNetNetstat('tests/netstat')
        else:
            self.stats = ProcNetNetstat()

    def run(self):
        while True:
            stats = self.stats.run()
            data = [{'agentKey': self.agent_key, 'plugins': {'ProcNetNetstat': stats}, 'tA': time.mktime(datetime.datetime.utcnow().timetuple())}]
            self._post_to_api(data)
            print stats
            time.sleep(5)

    def _post_to_api(self, data):
        url = '%s?deviceId=%s&apiKey=%s&account=%s' % (self.api_host, self.device_id, self.api_key, self.account)
        response = requests.post(
            url,
            auth=(self.username, self.password),
            data={'payload': json.dumps(data)})
        if response.ok:
            print response.content
        else:
            print 'error posting to api'

if __name__ == '__main__':
    usage = 'usage: %prog [options]'
    parser = OptionParser(usage=usage)
    parser.add_option('-u', '--username', dest='username', help='Server Density username')
    parser.add_option('-p', '--password', dest='password', help='Server Density password')
    parser.add_option('-a', '--account', dest='account', help='Server Density account (*.serverdensity.com)')
    parser.add_option('-k', '--key', dest='api_key', help='Server Density API key')
    parser.add_option('-d', '--deviceid', dest='device_id', help='device ID')
    parser.add_option('-g', '--agentkey', dest='agent_key', help='device agent key')
    parser.add_option('-o', '--host', dest='api_host', help='Server Density API host')
    (options, args) = parser.parse_args()

    if options.username and options.password and options.account and options.api_key and options.device_id and options.agent_key and options.api_host:
        app = App(options.username, options.password, options.account, options.api_key, options.device_id, options.agent_key, options.api_host)
        app.run()
    else:
        parser.error('incorrect number of arguments')
        sys.exit(1)
        