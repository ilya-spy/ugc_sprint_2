from olap import ReplicatedOlapCluster
from olap import OLAP_VIEWS_CLUSTER, OLAP_VIEWS_PATH
from olap import OLAP_VIEWS_SCHEMA, OLAP_VIEWS_DB

if __name__ == "main":

    # init clickhouse olap cluster
    olap_cluster = ReplicatedOlapCluster(
        cluster=OLAP_VIEWS_CLUSTER,
        path=OLAP_VIEWS_PATH,
        db=OLAP_VIEWS_DB,
        schema=OLAP_VIEWS_SCHEMA
    )
