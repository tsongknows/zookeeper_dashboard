from datetime import datetime
from kazoo.client import KazooClient

from zookeeper_dashboard.common import get_zookeeper_servers

PERM_READ = 1
PERM_WRITE = 2
PERM_CREATE = 4
PERM_DELETE = 8
PERM_ADMIN = 16
PERM_ALL = PERM_READ | PERM_WRITE | PERM_CREATE | PERM_DELETE | PERM_ADMIN

TIMEOUT = 10.0

class ZKClient(object):
    def __init__(self, servers, timeout):
        self.connected = False
        print("Connecting to %s" % (servers))
        self.zk_client = KazooClient(hosts=servers)
        self.zk_client.start(timeout=timeout)

    def close(self):
        self.zk_client.stop()

    def get(self, path, watcher=None):
        return self.zk_client.get(path, watcher)

    def get_children(self, path, watcher=None):
        return self.zk_client.get_children(path, watcher)

    def get_acls(self, path):
        return self.zk_client.get_acls(path)


class ZNode(object):
    @staticmethod
    def dict_from_znode_stat(znode_stat):
        if znode_stat == None:
            return {}
        return {'aversion': znode_stat.aversion,
                'count': znode_stat.count,
                'created': znode_stat.created,
                'ctime': znode_stat.ctime,
                'cversion': znode_stat.cversion,
                'czxid': znode_stat.czxid,
                'dataLength': znode_stat.dataLength,
                'ephemeralOwner': znode_stat.ephemeralOwner,
                'index': znode_stat.index,
                'last_modified': znode_stat.last_modified,
                'last_modified_transaction_id': znode_stat.last_modified_transaction_id,
                'mtime': znode_stat.mtime,
                'mzxid': znode_stat.mzxid,
                'numChildren': znode_stat.numChildren,
                'pzxid': znode_stat.pzxid,
                'version': znode_stat.version}

    @staticmethod
    def dict_from_acl(acl):
        return {'acl_list': acl.acl_list,
                'count': acl.count,
                'id': acl.id,
                'index': acl.index,
                'perms': acl.perms}

    def __init__(self, path="/"):
        self.path = path
        zk = ZKClient(get_zookeeper_servers(), TIMEOUT)
        try:
            self.data, znode_stat = zk.get(path)
            self.stat = self.dict_from_znode_stat(znode_stat)

            self.stat['ctime'] = datetime.fromtimestamp(self.stat.get('ctime',0)/1000)
            self.stat['mtime'] = datetime.fromtimestamp(self.stat.get('mtime',0)/1000)
            self.children = zk.get_children(path) or []
            acl_list = zk.get_acls(path)[0] or []
            self.acls = map(self.dict_from_acl, acl_list)

            for acl in self.acls:
                perms = acl['perms']
                perms_list = []
                if perms & PERM_READ:
                    perms_list.append("PERM_READ")
                if perms & PERM_WRITE:
                    perms_list.append("PERM_WRITE")
                if perms & PERM_CREATE:
                    perms_list.append("PERM_CREATE")
                if perms & PERM_DELETE:
                    perms_list.append("PERM_DELETE")
                if perms & PERM_ADMIN:
                    perms_list.append("PERM_ADMIN")
                if perms & PERM_ALL == PERM_ALL:
                    perms_list = ["PERM_ALL"]
                acl['perm_list'] = perms_list
        finally:
            zk.close()

    def path_parts(self):
        url = '/tree'
        yield 'Home', url
        for node in self.path[1:].split('/'):
            if node:
                url += '/%s' % node
                yield node, url
