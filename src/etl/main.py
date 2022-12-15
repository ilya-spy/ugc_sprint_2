import asyncio

from etl import extractor, loader, manager, transformer
from db.kafka.consumer import get_kafka_consumer


async def main():
    consumer =  get_kafka_consumer()
    await consumer.start()

    extract = extractor.get_extractor(extractor=consumer)
    transform = transformer.get_transformer()
    load = loader.get_loader()

    manage = manager.Manager(
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
