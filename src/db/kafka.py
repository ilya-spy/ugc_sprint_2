from aiokafka.admin import AIOKafkaAdminClient as KafkaAdminClient
from aiokafka.admin import NewTopic


async def kafka_init():
    """setting up kafka"""
    admin = KafkaAdminClient(
        bootstrap_servers="localhost:29092",  # TODO: забирать из конфигов
        client_id="test",
    )

    topics = await admin.list_topics()

    for_creation = _check_topic_existence(
        exists=topics, for_creation=["user_watching_progress"]
    )

    await create_topics(kafka_admin=admin, topic_names=for_creation)


def _check_topic_existence(exists: list[str], for_creation: list[str]) -> list[str]:
    """Func creates a list of topic names that doesn't exist already"""
    for existing_t in exists:
        if existing_t in for_creation:
            for_creation.pop(for_creation.index(existing_t))

    return for_creation


async def create_topics(kafka_admin: KafkaAdminClient, topic_names):
    """Func creates"""
    topics_list = [
        NewTopic(name=tn, num_partitions=10, replication_factor=1) for tn in topic_names
    ]
    await kafka_admin.create_topics(topics_list)


class BootstrapServers:
    bootstrap_servers = ["localhost:29092"]  # TODO: забирать из конфигов
