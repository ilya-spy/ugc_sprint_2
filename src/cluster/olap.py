import uuid

from core.config import config
from core.logging import get_logger, setup_logger

from db.clickhouse.manager import (
    ClickHouseClient,
    ClickHouseDistributedProxyTable,
    ClickHouseReplicatedTable,
    IDistributedOLAPData,
)

logger = get_logger(__name__)
logger = setup_logger(logger)


class ReplicatedOlapCluster:
    """Класс создаёт и поддерживает кластер из ClickHouse серверов"""

    def init_node(self, idx: int, node: str):
        """Инициализация отдельной ноды кластера"""
        host = f"{self.cluster}-{node}"
        logger.info("Init node %d: %s on host %s", idx, node, host)

        client = ClickHouseClient(host=host, port=9000, cluster=self.cluster)

        logger.info("Create shard database")
        client.create_distributed_db("shard")

        logger.info("Create replica database")
        client.create_distributed_db("replica")

        return client

    def init_table(
        self, node: ClickHouseClient, db: str, shard: str, replica: str = ""
    ):
        """Инициализация распределенной таблицы на ноде кластера"""
        common_params = {
            "name": config.olap.table,
            "schema": config.olap.scheme,
            "partition": config.olap.partition,
            "replica": replica,
            "root": config.olap.path,
            "shard": shard,
            "key": config.olap.orderby,
        }
        if replica:
            logger.info("Create replicated table: %s", replica)
            table = ClickHouseReplicatedTable(**common_params)
        else:
            logger.info(
                "Finalize distributed table: %s on %s", config.olap.table, self.cluster
            )
            table = ClickHouseDistributedProxyTable(
                **common_params, cluster=self.cluster
            )

        # Запросить создание выбранной таблицы или прокси
        node.create_distributed_table(db, table)
        return table

    def __init__(
        self, cluster: str, path: str, name: str, schema: str, shards: int = 2
    ) -> None:
        self.cluster = cluster
        self.path = path
        self.shards = shards
        self.name = name
        self.schema = schema

        if shards % 2 != 0:
            raise TypeError("Even number of shards is required for replication")

        self.shardnames = list(
            map(lambda idx: "shard" + str(idx), range(1, self.shards + 1))
        )
        self.nodenames = list(
            map(lambda idx: "node" + str(idx), range(1, self.shards + 1))
        )

        self.node = []
        for idx, name in enumerate(self.nodenames):
            node: ClickHouseClient = self.init_node(idx, name)
            self.node.append(node)

            #  Build replication topology out of pairs of nodes     #

            #  Node  1    Node  2    ...  Node  N-1    Node  N      #
            #  Shard 1    Shard 2    ...  Shard N-1    Shard N      #
            #  Replica 2  Replica 1  ...  Replica N    Replica N-1  #

            # add master table shard on current node
            self.init_table(
                node,
                config.olap.db_shard,
                self.shardnames[idx],
                self.shardnames[idx] + "_master",
            )

            # setup first node in a pair to be replicated on the next sibling
            if idx % 2 == 0:
                self.init_table(
                    node,
                    config.olap.db_replica,
                    self.shardnames[idx + 1],
                    self.shardnames[idx + 1] + "_replica",
                )

            # setup last node in a pair to be replicated on the previous sibling
            if idx % 2 == 1:
                self.init_table(
                    node,
                    config.olap.db_replica,
                    self.shardnames[idx - 1],
                    self.shardnames[idx - 1] + "_replica",
                )

            # setup distributed table proxy frontend to route between shard and replica
            frontend_table = self.init_table(
                node, config.olap.db_default, self.shardnames[idx]
            )

            # generate some random data to check shards distribution
            values = IDistributedOLAPData(
                [
                    f"('{uuid.uuid4()}', '{uuid.uuid4()}', '{uuid.uuid4()}', 100, now())"
                    for _ in range(config.olap.populate)
                ]
            )

            node.insert_into_table("default", frontend_table, (values))


def init_cluster():
    """init clickhouse olap cluster"""
    return ReplicatedOlapCluster(
        cluster=config.olap.cluster,
        path=config.olap.path,
        name=config.olap.table,
        schema=config.olap.scheme,
        shards=4,
    )

if __name__ == "__main__":
    olap_cluster = init_cluster()
