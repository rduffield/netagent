class ProcNetNetstat:
    def __init__(self):
        pass
    
    def run(self):
        dat = {}
        for line in open('/proc/net/netstat','r').readlines():
            line = line.split()
            name = line[0]
            line.remove(name)
            name = name.split(':')[0]
            if name not in dat:
                dat[name] = line
            else:
                dat[name] = dict(zip(dat[name], line))
        return dat
