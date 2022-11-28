if __name__ == "__main__":
    import uuid

    from kafka_messaging import WatchingProgBaseConsumer, WatchingProgressProducer

    prod = WatchingProgressProducer()
    cons = WatchingProgBaseConsumer()

    prod.send(progress="33", user_id=uuid.uuid4(), movie_id=uuid.uuid4())

    a = cons.consume()

    print(a.value.decode())
