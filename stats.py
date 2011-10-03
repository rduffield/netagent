class ProcNetNetstat:
    def __init__(self, netstat='/proc/net/netstat'):
        self.netstat = netstat
    
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
        return dat.get('TcpExt')
