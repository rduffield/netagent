class ProcNetNetstat:
    def __init__(self, netstat='/proc/net/netstat'):
        self.netstat = netstat

    def _floatify(self, key):
        self.dat.get('TcpExt')[key] = float(self.dat.get('TcpExt').get(key))

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
        map(self._floatify, dat.get('TcpExt').keys())
        return dat.get('TcpExt')
