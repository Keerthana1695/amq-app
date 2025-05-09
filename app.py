from flask import Flask, request
from proton import Message
from proton.reactor import Container
import os

app = Flask(__name__)

class Sender(Container):
    def __init__(self, amq_url, queue, body):
        super().__init__(self)
        self.amq_url = amq_url
        self.queue = queue
        self.body = body

    def on_start(self, event):
        conn = event.container.connect(self.amq_url)
        event.container.create_sender(conn, self.queue)

    def on_sendable(self, event):
        msg = Message(body=self.body)
        event.sender.send(msg)
        event.connection.close()

@app.route('/send')
def send():
    msg = request.args.get('msg', 'Hello from OpenShift!')
    amq_url = os.environ.get('AMQ_URL', 'amqp://amq-broker:5672')
    queue = os.environ.get('AMQ_QUEUE', 'example-queue')

    sender = Sender(amq_url, queue, msg)
    sender.run()
    return f"✅ Sent to {queue}: {msg}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
