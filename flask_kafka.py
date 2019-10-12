from kafka import KafkaProducer, KafkaConsumer, TopicPartition
from flask import jsonify
import datetime
import json


class Kafka:
    def __init__(self, app):
        print("Initializing Flask_kafka module...")
        self.app = app
        print("Flask_kafka Initialized.")

    def sendMessage(self, request):
        address = '192.168.30.91:9092'
        req = request.json
        attrsStr = ['topic', 'message', 'key',
                    'partition', 'headers', 'timestamp_ms']
        topic, message, key, partition, headers, timestamp_ms = (
            None for _ in range(6))

        '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                Kafka Cluster Config
        '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        if 'address' in req:
            address = req['address']
        producer = KafkaProducer(
            bootstrap_servers=address, api_version=(0, 11))

        '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                    MUST HAVES
        '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        topic = req['topic']
        message = json.dumps(req['message']).encode()

        '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                    OPTIONALS
        '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        if 'key' in req:
            key = req['key'].encode()       # Not Required
        if 'partition' in req:
            partition = req['partition']    # 0 by default if left blank
        if 'headers' in req:
            headers = req['headers']        # Not Required
        if 'timestamp_ms' in req:
            # Timestamp can be auto-generated.
            timestamp_ms = req['timestamp_ms']

        res = producer.send(topic, value=message, key=key, headers=headers,
                            partition=partition, timestamp_ms=timestamp_ms).get(timeout=10)
        producer.close(timeout=10)
        return(jsonify({
            "code": "200",
            "message": "success",
            "kafka_message": {
                    "topic": res.topic,
                    "partition": res.partition,
                    "offset": res.offset,
                    "timestamp": res.timestamp
            },
            "timestamp": str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        }
        ))


    @app.route('/kafka/receive_message/', methods=["POST"])
    def receive_messages(self, request):

        # Handle request data.
        req = request.json
        must_haves = ['address','topic']
        for key in must_haves:
            if key not in req:
                return jsonify({
                    'code': 110402,
                    'message': "You don't have " + key + " in your request."
                })
        topic = req['topic']
        address = req['address']
        num_messages = req['num_messages'] if "num_messages" in req else 1
        partition = req['partition'] if 'partition' in req else 0


        # Create kafka consumer.
        consumer = KafkaConsumer(topic,
                                auto_offset_reset='latest', bootstrap_servers=address)
        # Obtain partition info.
        consumer.partitions_for_topic(topic)

        # Get earliest and latest offsets.
        tp = TopicPartition(topic=topic, partition=0)
        earliest_offset = consumer.beginning_offsets(consumer.assignment())[tp]
        latest_offset = consumer.position(tp)

        # If user tries to read data before the earliest, set offset to earliest.
        consumer.seek(tp, max([latest_offset-num_messages,earliest_offset]))

        # Handle messages.
        messages = []
        for message in consumer:
            messages.append({
                "partition": message.partition,
                "offset": message.offset,
                "timestamp": message.timestamp,
                "key": str(message.key),
                "message": str(message.value)
            })
            if message.offset == latest_offset-1:
                break

        return jsonify({
            "assignment": consumer.assignment(),
            "subscription": consumer.subscription(),
            "message": messages
        })