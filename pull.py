from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'projects/pluralsight-demos-475513/subscriptions/pull-test'

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

with subscriber:
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()