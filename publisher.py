import pika
from dotenv import load_dotenv
import os
import json
from typing import Dict
load_dotenv()

class RabbitmqPublisher:
    def __init__(self) -> None:
        self.__host = "localhost"
        self.__port = 5672
        self.__username = os.getenv("RABBITMQ_USERNAME", "guest")
        self.__password = os.getenv("RABBITMQ_PASSWORD", "guest")
        self.__exchange ="my_exchange"
        self.__routing_key = "RK"
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
        return channel
    
    def send_message(self, body:Dict):
        self.__channel.basic_publish(
            exchange=self.__exchange,
            routing_key=self.__routing_key,
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
rabbitmq_publisher = RabbitmqPublisher()
rabbitmq_publisher.send_message({"ola": "Mundo"})