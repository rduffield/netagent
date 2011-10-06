class ProcNetNetstat:
    def __init__(self, netstat='/proc/net/netstat', key='TcpExt'):
        self.netstat = netstat
        self.key = key

    def _floatify(self, key):
        for sub_key in self.dat.get(key):
            self.dat.get(key)[sub_key] = float(self.dat.get(key).get(sub_key))

    def run(self):
        dat = {}
        f = open(self.netstat, 'r')
        for line in f.readlines():
            line = line.split()
            name = line[0]
            line.remove(name)
            name = name.split(':')[0]
            if name not in dat:
                dat[name] = line
            else:
                dat[name] = dict(zip(dat[name], line))
        f.close()
        self.dat = dat
        map(self._floatify, dat.keys())
        return dat
