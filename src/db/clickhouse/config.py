from pydantic import BaseSettings, Field


class ClickHouseConfig(BaseSettings):
    host: str = Field(default="localhost")
    port: int = Field(default=9000)
    cluster: str = Field(default="clickhouse")
    path: str = Field(default="/clickhouse/tables")
    db_default: str = Field(default="default")
    db_shard: str = Field(default="shard")
    db_replica: str = Field(default="replica")
    table: str = Field(default="main")
    scheme: str = Field(default="()")
    partition: str = Field(default="")
    orderby: str = Field(default="")
    populate: int = Field(default=0)

    class Config:
        env_prefix = "olap_views_"
        env_nested_delimiter = "_"