from celery import Celery
from time import sleep
from random import randint
import os
from dotenv import load_dotenv
load_dotenv()

username = os.getenv("RABBITMQ_USERNAME", "guest")
password = os.getenv("RABBITMQ_PASSWORD", "guest")


app = Celery('task',broker=f"amqp://{username}:{password}@localhost:5672//")

@app.task
def hello(nome : str):
    sleep(5)
    if randint(1, 4) == 1:
        raise Exception('Deu ruim')
    return "hello {}".format(nome)