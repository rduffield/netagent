#!/usr/bin/env python

import datetime
import json
import requests
import time
from optparse import OptionParser

class Poster(object):
    """
    Class for posting results to Server Density.
    """
    def __init__(self, username, password, account, api_key, device_id, agent_key, api_host, log_file, plugin='ProcNetNetstat'):
        super(Poster, self).__init__()
        self.username = username
        self.password = password
        self.account = account
        self.api_key = api_key
        self.device_id = device_id
        self.agent_key = agent_key
        self.api_host = api_host
        self.log_file = log_file
        self.plugin = plugin
        self.position = 0

    def run(self):
        start = datetime.datetime.utcnow()
        data = []
        while True:
            f = open(self.log_file, 'r')
            f.seek(self.position, 0)
            contents = f.readlines()
            now = datetime.datetime.utcnow()
            for content in contents:
                self.position = f.tell()
                data.append({'agentKey': self.agent_key, 'plugins': {self.plugin: json.loads(content)}, 'tA': time.mktime(datetime.datetime.utcnow().timetuple())})
                difference = now - start
                if difference.seconds >= 60:
                    self._post_to_api(data)
                    start = now
                    data = []
            f.close()
            time.sleep(1)

    def _post_to_api(self, data):
        url = '%s?deviceId=%s&apiKey=%s&account=%s' % (self.api_host, self.device_id, self.api_key, self.account)
        response = requests.post(
            url,
            auth=(self.username, self.password),
            data={'payload': json.dumps(data)})

if __name__ == '__main__':
    usage = 'usage: %prog [options] log_file'
    parser = OptionParser(usage=usage)
    parser.add_option('-u', '--username', dest='username', help='Server Density username')
    parser.add_option('-p', '--password', dest='password', help='Server Density password')
    parser.add_option('-a', '--account', dest='account', help='Server Density account (*.serverdensity.com)')
    parser.add_option('-k', '--key', dest='api_key', help='Server Density API key')
    parser.add_option('-d', '--deviceid', dest='device_id', help='device ID')
    parser.add_option('-g', '--agentkey', dest='agent_key', help='device agent key')
    parser.add_option('-o', '--host', dest='api_host', help='Server Density API host')
    parser.add_option('-l', '--plugin', dest='plugin', help='plugin name')
    (options, args) = parser.parse_args()

    if options.plugin:
        plugin = options.plugin
    else:
        plugin = 'ProcNetNetstat'

    if options.username and options.password and options.account and options.api_key and options.device_id and options.agent_key and options.api_host and len(args):
        p = Poster(options.username, options.password, options.account, options.api_key, options.device_id, options.agent_key, options.api_host, args[0], plugin=plugin)
        p.run()
    else:
        parser.error('incorrect number of arguments')
        sys.exit(1)
