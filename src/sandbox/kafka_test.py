from db.kafka_messaging import consumers, producers

if __name__ == "__main__":
    import uuid

    prod = producers.WatchingProgressProducer()
    cons = consumers.WatchingProgBaseConsumer()

    prod.send(progress="33", user_id=uuid.uuid4(), movie_id=uuid.uuid4())

    a = cons.consume()

    print(a.value.decode())
