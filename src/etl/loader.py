import uuid
from functools import lru_cache

from db.clickhouse import ClickHouseClient, IDistributedOLAPData, IDistributedOLAPTable
from etl.models import WatchingProgressClickHouseSchema as CHSchema


class Loader:
    def __init__(self):
        self.ch_client = ClickHouseClient(
            # TODO: данные из конфигов
        )

    def load(self, ch_msg: CHSchema):
        self.ch_client.insert_into_table(
            db="default",
            table=IDistributedOLAPTable(
                name="olap_views",
                schema="(id UUID, user_id UUID, film_id UUID, frame Int64, event_time DateTime)",
            ),
            data=IDistributedOLAPData(
                [
                    f"('{uuid.uuid4()}',  '{ch_msg.user_id}', '{ch_msg.film_id}', {ch_msg.frame}, {ch_msg.event_time})"
                ]
            ),
        )


@lru_cache
def get_loader() -> Loader:
    return Loader()
