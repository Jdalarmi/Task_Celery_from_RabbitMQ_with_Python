import pika
import os
from dotenv import load_dotenv
load_dotenv()

connection_parameters = pika.ConnectionParameters(
    host="localhost",
    port="5672",
    credentials=pika.PlainCredentials(
        username=os.getenv("RABBITMQ_USERNAME", "guest"),
        password=os.getenv("RABBITMQ_PASSWORD", "guest")
    )
)

channel = pika.BlockingConnection(connection_parameters).channel()

channel.basic_publish(
    exchange="my_exchange",
    routing_key="",
    body="EstaOuvindo",
    properties=pika.BasicProperties(
        delivery_mode=2
    )
)