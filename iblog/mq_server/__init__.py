import threading

from iblog import target
from iblog.issue import Issue


class ConsumerOfKafka(object):
    def __init__(self, topic, group_id, servers):
        from kafka import KafkaConsumer
        self.topic = topic
        self.group_id = group_id
        if servers:
            self.servers = servers
        else:
            self.servers = 'localhost:9092'
        consumer = KafkaConsumer(self.topic, group_id=self.group_id, bootstrap_servers=self.servers)
        self.consumer = consumer

    def run(self):
        for msg in self.consumer:
            # issue = Issue()
            # issue.__dict__.update()
            # target.sync_create(issue)
            print(msg)


class ConsumerOfAmqp(object):
    def __init__(self, queue, servers):
        self.queue = queue
        if servers:
            self.servers = servers
        else:
            self.servers = 'localhost:5672'
        import pika
        server_list = [pika.ConnectionParameters(host=s.split(':')[0], port=int(s.split(':')[1]))
                       for s in servers.split(',')]
        parameters = tuple(server_list)
        connection = pika.BlockingConnection(parameters)
        # 链接
        self.connection = connection

    def run(self):
        channel = self.connection.channel()
        for method_frame, properties, body in channel.consume(queue=self.queue):
            # Display the message parts and acknowledge the message
            print(method_frame, properties, body)
            channel.basic_ack(method_frame.delivery_tag)

        self.connection.close()


class MqServer(threading.Thread):
    def __init__(self, mq, queue, servers, topic, group_id):
        super().__init__()
        self.mq = mq
        if self.mq == 'kafka':
            self.server = ConsumerOfKafka(topic=topic, group_id=group_id, servers=servers)
        else:
            self.server = ConsumerOfAmqp(queue=queue, servers=servers)

    def run(self):
        self.server.run()
