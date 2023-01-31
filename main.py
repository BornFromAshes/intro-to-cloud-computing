import pika
import flask
import json
import dependencies


def sender(tag):
    url = "your rabbit mq url"
    connection = pika.BlockingConnection(pika.URLParameters(url))
    channel = connection.channel()
    channel.queue_declare(queue='Advertisements')
    channel.basic_publish(exchange='', routing_key='Advertisements', body=tag)
    print(tag + " sent")


app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    json_dump = json.dumps({"response": "To post an add use /postad and to see how your ad is doing use /showad"})
    return json_dump


@app.route('/postad/', methods=['GET', 'POST'])
def post_ad():
    in_email = str(flask.request.args.get('email'))
    in_path = str(flask.request.args.get('path'))
    in_desc = str(flask.request.args.get('description'))

    ad = dependencies.Advertisement(in_email, in_desc, in_path)
    ad.post()
    post_id = ad.id
    s3 = dependencies.S3()
    s3.upload(in_path, str(post_id) + ".jpg")
    sender(str(post_id))
    json_dump = json.dumps({"response": "Your advertisement has been created", "id": ad.id})
    return json_dump


@app.route('/showad/', methods=['GET', 'POST'])
def show_ad():
    in_post_id = int(flask.request.args.get('id'))
    db = dependencies.DataBase()
    state = db.show(in_post_id)["state"]
    if state == "pending":
        json_dumps = json.dumps({"response": "your advertisement is in check queue"})
    elif state == "accepted":
        json_dumps = json.dumps({"response": "your advertisement is accepted!"})
    else:
        json_dumps = json.dumps({"response": "your advertisement is rejected!"})
    return json_dumps


if __name__ == "__main__":
    app.run(debug=True)
