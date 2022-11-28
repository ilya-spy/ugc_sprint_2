from kafka.admin import KafkaAdminClient, NewTopic


def kafka_init():
    """setting up kafka"""
    admin = KafkaAdminClient(
        bootstrap_servers=["localhost:29092"],  # TODO: забирать из конфигов
        client_id="test",
    )

    for_creation = _check_topic_existence(
        exists=admin.list_topics(), for_creation=["user_watching_progress"]
    )

    create_topics(kafka_admin=admin, topic_names=for_creation)


def _check_topic_existence(
    exists: list[NewTopic], for_creation: list[str]
) -> list[str]:
    """Func creates a list of topic names that doesn't exist already"""
    for existing_t in exists:
        if existing_t.name in for_creation:
            for_creation.pop(for_creation.index(existing_t.name))

    return for_creation


def create_topics(kafka_admin: KafkaAdminClient, topic_names):
    """Func creates"""
    topics_list = [
        NewTopic(name=tn, num_partitions=10, replication_factor=1) for tn in topic_names
    ]
    kafka_admin.create_topics(topics_list)


class BootstrapServers:
    bootstrap_servers = ["localhost:29092"]  # TODO: забирать из конфигов
