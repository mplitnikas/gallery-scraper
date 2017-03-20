import pika
import config

class Requestor:

	def __init__(self, uri):
		self.create_connection(uri)
		self.setup_consume()

	def create_connection(self, uri):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(uri))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='requests')
		self.channel.queue_declare(queue='responses')

	def __enter__(self):
		return self

	def setup_consume(self):
		self.channel.basic_consume(self.callback,
									queue='requests',
									no_ack=True)
		print 'beginning consumer'
		self.channel.start_consuming()

	def callback(self, ch, method, properties, body):
		print 'received %r' % body


	def __exit__(self):
		self.connection.close()

if __name__ == '__main__':
	with Requestor(config.rabbit_uri) as rq:
		# just need to call the init method to start things off
		pass