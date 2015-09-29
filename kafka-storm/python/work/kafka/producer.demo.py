#! coding: utf-8
'''kafka-python usage'''

KAFKA_SERVER = '10.13.186.251:9092'

def simple_producer():
    '''simple producer'''
    from kafka import SimpleProducer, KafkaClient

    # To send messages synchronously
    kafka = KafkaClient(KAFKA_SERVER)
    producer = SimpleProducer(kafka)

    # Note that the application is responsible for encoding messages to type bytes
    producer.send_messages(b'topic1', b'some message')
    producer.send_messages(b'topic1', b'this method', b'is variadic')
    # Send unicode message
    producer.send_messages(b'topic1', u'你怎么样?'.encode('utf-8'))

def asynchronous_mode():
    '''Asynchronous Mode'''
    from kafka import SimpleProducer, KafkaClient
    import logging

    # To send messages asynchronously
    kafka = KafkaClient(KAFKA_SERVER)
    producer = SimpleProducer(kafka, async=True)
    producer.send_messages(b'topic1', b'async message')

    # To wait for acknowledgements
    # ACK_AFTER_LOCAL_WRITE : server will wait till the data is written to
    #                         a local log before sending response
    # ACK_AFTER_CLUSTER_COMMIT : server will block until the message is committed
    #                            by all in sync replicas before sending a response
    producer = SimpleProducer(kafka, async=False,
                              req_acks=SimpleProducer.ACK_AFTER_LOCAL_WRITE,
                              ack_timeout=2000,
                              sync_fail_on_error=False)

    responses = producer.send_messages(b'topic1', b'another message')
    for response in responses:
        logging.info(response.offset)

    # To send messages in batch. You can use any of the available
    # producers for doing this. The following producer will collect
    # messages in batch and send them to Kafka after 20 messages are
    # collected or every 60 seconds
    # Notes:
    # * If the producer dies before the messages are sent, there will be losses
    # * Call producer.stop() to send the messages and cleanup
    producer = SimpleProducer(kafka, async=True,
                              batch_send_every_n=20,
                              batch_send_every_t=60)

def keyed_messages():
    '''Keyed messages'''
    from kafka import (KafkaClient, KeyedProducer,
    Murmur2Partitioner, RoundRobinPartitioner)

    kafka = KafkaClient(KAFKA_SERVER)

    # HashedPartitioner is default (currently uses python hash())
    producer = KeyedProducer(kafka)
    producer.send_messages(b'topic1', b'key1', b'some message')
    producer.send_messages(b'topic1', b'key2', b'this methode')

    # Murmur2Partitioner attempts to mirror the java client hashing
    producer = KeyedProducer(kafka, partitioner=Murmur2Partitioner)

    # Or just produce round-robin (or just use SimpleProducer)
    producer = KeyedProducer(kafka, partitioner=RoundRobinPartitioner)


simple_producer()
