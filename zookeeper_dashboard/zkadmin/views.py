from django.shortcuts import render_to_response

from zookeeper_dashboard.zkadmin.models import ZKServer
from zookeeper_dashboard.common import get_zookeeper_servers_as_list, get_zookeeper_server


def index(request):
    zookeeper_servers = get_zookeeper_servers_as_list()
    server_data = []
    for i, server in enumerate(zookeeper_servers):
        zkserver = ZKServer(server)
        zkserver.id = i
        server_data.append(zkserver)

    return render_to_response('zkadmin/index.html',
                              {'ZOOKEEPER_SERVERS': zookeeper_servers,
                               'server_data': server_data})

def detail(request, server_id):
    server_data = ZKServer(get_zookeeper_server(server_id))
    server_data.id = server_id
    return render_to_response('zkadmin/detail.html',
                              {'server_data':server_data})
