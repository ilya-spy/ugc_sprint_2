import uuid
from functools import lru_cache
from typing import AsyncIterator

from core.config import config
from db.clickhouse.ch_manager import (
    ClickHouseClient,
    IDistributedOLAPData,
    IDistributedOLAPTable,
)
from etl.models import WatchingProgressClickHouseSchema as CHSchema


class Loader:
    def __init__(self):
        self.ch_client = ClickHouseClient(
            host=config.olap.host, port=config.olap.port, cluster=config.olap.cluster
        )

    async def load(self, ch_msgs: AsyncIterator[CHSchema]):
        """Insert batches of etl messages"""
        data = [
            f"('{uuid.uuid4()}', '{ch_msg.user_id}', '{ch_msg.film_id}', {ch_msg.frame}, {ch_msg.event_time})"
            async for ch_msg in ch_msgs
            if ch_msg is not None
        ]
        if not data:
            return

        self.ch_client.insert_into_table(
            db=config.olap.db_default,
            table=IDistributedOLAPTable(
                name=config.olap.table,
                schema=config.olap.scheme,
            ),
            data=IDistributedOLAPData(values=data),
        )


@lru_cache
def get_loader() -> Loader:
    """Singleton Loader instance"""
    return Loader()
