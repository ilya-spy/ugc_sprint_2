from config import config
from olap import ReplicatedOlapCluster

def init_cluster():
    """init clickhouse olap cluster"""
    return ReplicatedOlapCluster(
        cluster=config.olap.cluster,
        path=config.olap.path,
        name=config.olap.table,
        schema=config.olap.scheme,
        shards=4
    )

if __name__ == '__main__':
    olap_cluster = init_cluster()
