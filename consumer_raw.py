import pika
from dotenv import load_dotenv
import os 
load_dotenv()

def minha_callback(ch, method, properties, body):
    print(body)

connection_parameters = pika.ConnectionParameters(
    host="localhost",
    port="5672",
    credentials=pika.PlainCredentials(
        username=os.getenv("RABBITMQ_USERNAME", "guest"),
        password=os.getenv("RABBITMQ_PASSWORD", "guest")
    )
)

channel = pika.BlockingConnection(connection_parameters).channel()
channel.queue_declare(
    queue="data_queue",
    durable=True
)
channel.basic_consume(
    queue="data_queue",
    auto_ack=True,
    on_message_callback=minha_callback
)


print(f'Listen RabbitMq on Port 5672')
channel.start_consuming()