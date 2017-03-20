import pika
import config

class Publisher:

	def __init__(self):
		self.create_connection(config.rabbit_uri)

	def create_connection(self, uri):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(uri))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='requests')
		self.channel.queue_declare(queue='responses')

	def __enter__(self):
		return self

	def publish(self, body):
		self.channel.basic_publish(exchange='',
									routing_key='requests',
									body=body)

	def __exit__(self, exc_type, exc_value, traceback):
		self.connection.close()

if __name__ == '__main__':
	with Publisher() as pb:
		pb.publish('Hello there')