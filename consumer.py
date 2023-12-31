import pika
from dotenv import load_dotenv
import os
load_dotenv()

class RabbitmqConsumer:
    def __init__(self, callback) -> None:
        self.__host = "localhost"
        self.__port = 5672
        self.__username = os.getenv("RABBITMQ_USERNAME", "guest")
        self.__password = os.getenv("RABBITMQ_PASSWORD", "guest")
        self.__queue = "data_queue3"
        self.__callback = callback
        self.__channel = self.__create_channel()

    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username,
                password=self.__password
            )
        )

        channel = pika.BlockingConnection(connection_parameters).channel()
        channel.queue_declare(
            queue=self.__queue,
            durable=True,
            arguments={
                "x-overflow":"reject-publish",
            }
        )
        channel.basic_consume(
            queue=self.__queue,
            auto_ack=True,
            on_message_callback=self.__callback
        )

        return channel
    
    def start_consuming(self):
        print(f'Listen RabbitMq on Port 5672')
        self.__channel.start_consuming()       

def minha_callback(ch, method, properties, body):
    print(body)

rabbitmq_consumer = RabbitmqConsumer(minha_callback)
rabbitmq_consumer.start_consuming()