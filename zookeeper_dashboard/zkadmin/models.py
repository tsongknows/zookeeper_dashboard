import re
from six import StringIO
import telnetlib

OP_READ = 1
OP_WRITE = 4
OP_CONNECT = 8
OP_ACCEPT = 16

class Session(object):
    def __init__(self, session):
        ipv4 = re.search('/(\d+\.\d+\.\d+\.\d+):(\d+)\[(\d+)\]\((.*)\)', session)
        ipv6 = re.search('/(\d+:\d+:\d+:\d+:\d+:\d+:\d+:\d+):(\d+)\[(\d+)\]\((.*)\)', session)

        if ipv4:
            m = ipv4
        elif ipv6:
            m = ipv6
        else:
            self.host = "COULD NOT PARSE"
            self.post = "COULD NOT PARSE"
            self.interest_ops = "COULD NOT PARSE"
            self.__dict__ = {}
            return

        self.host = m.group(1)
        self.port = m.group(2)
        self.interest_ops = m.group(3)
        for d in m.group(4).split(","):
            k,v = d.split("=")
            self.__dict__[k] = v

class ZKServer(object):
    def __init__(self, server):
        self.host, self.port = server.split(':')
        try:
            stat = self.send_cmd('stat\n')
            envi = self.send_cmd('envi\n')
            sio = StringIO(stat)
            line = sio.readline()
            if 'not currently serving requests' in line:
                raise Exception("This ZooKeeper instance is not currently serving requests")
        except:
            self.mode = "Unreachable"
            self.sessions = []
            self.version = "Unknown"
            return

        m = re.search('.*: (\d+\.\d+\.\d+)-.*', line)
        self.version = m.group(1)
        sio.readline()
        self.sessions = []
        for line in sio:
            if not line.strip():
                break

            self.sessions.append(Session(line.strip()))
        for line in sio:
            attr, value = line.split(':')
            attr = attr.strip().replace(" ", "_").replace("/", "_").lower()
            self.__dict__[attr] = value.strip()

        self.min_latency, self.avg_latency, self.max_latency = self.latency_min_avg_max.split("/")

        self.envi = []
        sio = StringIO(envi)
        for line in sio:
            if not line.strip(): break
            attr, equ, value = line.partition("=")
            if not equ: continue
            self.envi.append((attr, value))

    def send_cmd(self, cmd):
        tn = telnetlib.Telnet(self.host, self.port)

        tn.write(cmd)
        # Was getting a weird error where first read_all failed
        try:
            result = tn.read_all()
        except:
            result = tn.read_all()
        tn.close()

        return result
