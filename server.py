import pika
import requests
import dependencies


def send_email(email, post_id, state):
    return requests.post(
        "mailgun api",
        auth=("api", "your auth key"),
        data={"from": "Mailgun Sandbox <your url>",
              "to": "<" + email + ">",
              "subject": "Your advertisement has been reviewed!",
              "text": "Your advertisement with the id of " + post_id + " has been " + state + "!"})


def image_tagging(path):
    api_key = 'your Imagga key'
    api_secret = 'your Imagga secret key'
    image_path = path

    response = requests.post(
        'https://api.imagga.com/v2/tags',
        auth=(api_key, api_secret),
        files={'image': open(image_path, 'rb')})
    js = response.json()['result']['tags']
    for i in js:
        if i['tag']['en'] == 'vehicle' and i['confidence'] > 50:
            return "accepted", js[0]['tag']['en']
    return "rejected", None


def receiver():
    url = "your rabbitMQ url"
    connection = pika.BlockingConnection(pika.URLParameters(url))
    channel = connection.channel()
    channel.queue_declare(queue='Advertisements')
    channel.basic_consume(queue='Advertisements', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


def callback(ch, method, properties, body):
    body = int(body)
    path = "C:/Users/parham/OneDrive/Desktop/" + str(body) + ".jpg"
    s3_obj = dependencies.S3()
    s3_obj.download(path, str(body) + ".jpg")
    print("file downloaded")
    state, category = image_tagging(path)
    db_obj = dependencies.DataBase()
    db_obj.update(body, state, category)
    print("database updated")
    send_email(db_obj.show(body)['email'], str(body), state)
    print("email sent")
    print("________________________________")


if __name__ == "__main__":
    receiver()

