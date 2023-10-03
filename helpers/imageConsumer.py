import pika
import json
import base64
from PIL import Image
from io import BytesIO
from deleteFiles import delete_images
from s3Aws import uploadImage
from imagComp import compareTwo

# Callback function to handle incoming messages
def callback(ch, method, properties, body):
    print(ch)
    try:
        # Decode the JSON message
        message = json.loads(body)
        print("id", message[-1])
        # Check if there are at least two images in the message
        if len(message) < 2:
            print("Received fewer than 2 images, cannot perform comparison.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        # Decode and process each image in the message
        image_list = []
        for image_info in message[:2]:
            image_data = image_info.get("image_data")
            # Decode the base64-encoded image data
            image_bytes = base64.b64decode(image_data)
            # Create a PIL Image object from the image data
            image = Image.open(BytesIO(image_bytes))
            # Append the image to the list
            image_list.append(image)

        # Check if there are at least two images in the list
        if len(image_list) < 2:
            print("Received fewer than 2 images, cannot perform comparison.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        # Perform image comparison using your existing function
        image_list[0].save("imagen1.jpg")
        image_list[1].save("imagen2.jpg")
        result = compareTwo("imagen1.jpg", "imagen2.jpg")
        if (result== "The same person appears in both images."):
            uploadImage("imagen1.jpg")
            uploadImage("imagen2.jpg")
        # Print the comparison result
        print(f"Image comparison result: {result}, id {message[-1]['id_sesion']}")        
        delete_images(["imagen1.jpg", "imagen2.jpg"])
        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message: {str(e)}")


def main():
    # Create a RabbitMQ connection and channel
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    # Declare the queue 
    channel.queue_declare(queue='image_queue')

    # Set the maximum number of unacknowledged messages
    channel.basic_qos(prefetch_count=1)

    # Register the callback function to handle incoming messages
    channel.basic_consume(queue='image_queue', on_message_callback=callback)

    print("Waiting for messages. To exit, press Ctrl+C")

    # Start consuming messages from the queue
    channel.start_consuming()

if __name__ == '__main__':
    main()
