import logging

from typing import List, Tuple

from db.clickhouse import ClickHouseClient, ClickHouseReplicatedTable


logger = logging.getLogger(__name__)

# Create logging handlers
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)

# Add handlers to the logger
logger.addHandler(c_handler)


# ClickHouse schema for storing viewing evetns
OLAP_VIEWS_SCHEMA = '(user_id Int64, film_id Int64, frame Int64, time DateTime)'
OLAP_VIEWS_CLUSTER = 'company_cluster'
OLAP_VIEWS_PATH = '/clickhouse/tables/'
OLAP_VIEWS_DB = 'views'


class ReplicatedOlapCluster:
    @staticmethod
    def init_node(cluster: str, node: str):
        host = f'{cluster}-{node}'
        logger.info('Init node %s on host: %s', node, host)

        client = ClickHouseClient(host=host, cluster=cluster)

        logger.info('Create shard database')
        client.create_distributed_db('shard')

        logger.info('Create replica database')
        client.create_distributed_db('replica')

        return client

    def __init__(self,
                 cluster: str,
                 path: str,
                 db: str,
                 schema: str,
                 shards: int = 2) -> None:
        self.cluster = cluster
        self.path = path
        self.shards = shards
        self.db = db
        self.schema = schema

        if shards % 2 != 0:
            raise('Even number of shards is required for replication')

        self.shardnames = list(
            map(lambda idx: 'shard' + str(idx), range(1, self.shards + 1))
        )
        self.nodenames = list(
            map(lambda idx: 'node' + str(idx), range(1, self.shards + 1))
        )
        
        self.node = []
        for name in self.nodenames:
            self.node.append(ReplicatedOlapCluster.init_node(self.cluster, name))

        #  Build replication topology out of pairs of nodes     #

        #  Node  1    Node  2    ...  Node  N-1    Node  N      #
        #  Shard 1    Shard 2    ...  Shard N-1    Shard N      #
        #  Replica 2  Replica 1  ...  Replica N    Replica N-1  #

        