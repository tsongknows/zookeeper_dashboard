import os

from django.conf import settings

def get_zookeeper_servers():
    return (
        os.getenv('ZOOKEEPER_SERVERS')
        or getattr(settings,'ZOOKEEPER_SERVERS')
    )

def get_zookeeper_servers_as_list():
    return get_zookeeper_servers().split(',')

def get_zookeeper_server(id):
    return get_zookeeper_servers_as_list()[id]
