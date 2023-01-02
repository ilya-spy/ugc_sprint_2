import asyncio

import sentry_sdk

from core.config import config
from db.kafka.kfk_consumer import get_kafka_consumer
from etl import extractor, loader, router, transformer

sentry_sdk.init(dsn=config.sentry.dsn)


async def main():
    """ETL entrypoint"""
    consumer = get_kafka_consumer()
    await consumer.start()

    extract = extractor.get_extractor(extractor=consumer)
    transform = transformer.get_transformer()
    load = loader.get_loader()

    manage = router.Manager(
        extractor_obj=extract,
        transformer_obj=transform,
        loader_obj=load,
    )

    try:
        await manage.start()
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
