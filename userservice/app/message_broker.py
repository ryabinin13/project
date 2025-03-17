# message_broker.py
import aio_pika

class MessageBroker:
    def __init__(self, rabbit_url):
        self.rabbit_url = rabbit_url
        self.connection = None
        self.channel = None 

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.rabbit_url)
        self.channel = await self.connection.channel()

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def publish_user_registered(self, user_id):
        if not self.channel:
            await self.connect()
        message_body = f"User registered with id: {user_id}"
        message = aio_pika.Message(body=message_body.encode())
        await self.channel.default_exchange.publish(message, routing_key="user_registered")
