#! coding: utf-8
'''kafka-python usage'''

KAFKA_SERVER = '10.13.186.251:9092'

def kafka_consumer():
    '''kafka consumer'''
    from kafka import KafkaConsumer

    # To consume messages
    consumer = KafkaConsumer('topic1',
                             group_id='my-group',
                             bootstrap_servers=[KAFKA_SERVER])
    for message in consumer:
        # message value is raw byte string -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                             message.offset, message.key,
                                             message.value))

def multiprocess_consumer():
    '''multiprocess consumer'''
    from kafka import KafkaClient, MultiProcessConsumer

    kafka = KafkaClient(KAFKA_SERVER)

    # This will split the number of partitions among two processes
    consumer = MultiProcessConsumer(kafka, b'my-group', b'topic1', num_procs=2)

    # This will spawn processes such that each handles 2 partitions max
    consumer = MultiProcessConsumer(kafka, b'my-group', b'topic1',
                                    partitions_per_proc=2)

    for message in consumer:
        print message

    for message in consumer.get_messages(count=5, block=True, timeout=4):
        print message


def low_level():
    '''low level'''
    from kafka import KafkaClient, create_message
    from kafka.protocol import KafkaProtocol
    from kafka.common import ProduceRequest

    kafka = KafkaClient(KAFKA_SERVER)

    req = ProduceRequest(topic=b'topic1', partition=1,
                         messages=[create_message(b'some message')])
    resps = kafka.send_produce_request(payloads=[req], fail_on_error=True)
    kafka.close()

    print resps[0].topic      # b'topic1'
    print resps[0].partition  # 1
    print resps[0].error      # 0 (hopefully)
    print resps[0].offset     # offset of the first message sent in this request

kafka_consumer()
# multiprocess_consumer()
# low_level()
