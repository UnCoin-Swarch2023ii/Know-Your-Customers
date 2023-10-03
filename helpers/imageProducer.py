import pika
import json
import base64

        
def send_images_to_queue(image1, image2,id_sesion ):
    with open(image1, 'rb') as image_file:
        image1_data = base64.b64encode(image_file.read()).decode('utf-8')

    with open(image2, 'rb') as image_file:
        image2_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Create a RabbitMQ connection and channel
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='image_queue')

    # Create a list with the image data
    message = [
        {"image_data": image1_data},
        {"image_data": image2_data},
        {"id_sesion": id_sesion}
    ]

    # Send the list as a single JSON message to the RabbitMQ queue
    channel.basic_publish(exchange='',routing_key='image_queue',body=json.dumps(message))
    print(" [x] Sent Images")

    connection.close()
