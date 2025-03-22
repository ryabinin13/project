import aio_pika


class BrokerProducerService:

    def __init__(self, channel, queue):
        self.channel = channel
        self.queue = queue


    async def publish_add_user_in_task(self, task_id, email):
        message_body = str(task_id) + " " + email
        message = aio_pika.Message(body=message_body.encode())
        await self.channel.default_exchange.publish(message, routing_key="user_email_from_team")