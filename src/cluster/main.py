from core.config import config

from .olap import ReplicatedOlapCluster


# TODO: move to olap.py
def init_cluster():
    """Init clickhouse olap cluster"""
    return ReplicatedOlapCluster(
        cluster=config.olap.cluster,
        path=config.olap.path,
        name=config.olap.table,
        schema=config.olap.scheme,
        shards=4,
    )


# TODO: do this like python cluster/olap.py
if __name__ == "__main__":
    olap_cluster = init_cluster()

# FIXME: remove this file
