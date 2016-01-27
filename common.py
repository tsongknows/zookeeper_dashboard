import os

def get_zookeeper_servers():
    return os.getenv('ZOOKEEPER_SERVERS') or getattr(settings,'ZOOKEEPER_SERVERS')
