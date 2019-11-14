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
        req = request.json
        attrsStr = ['topic', 'message', 'key',
                    'partition', 'headers', 'timestamp_ms']
        topic, message, key, partition, headers, timestamp_ms = (
            None for _ in range(6))

        if 'address' in req:
            address = req['address']
            producer = KafkaProducer(
                bootstrap_servers=address, api_version=(0, 11))
        else:
            return(jsonify({
                "code": 110403,
                "message": "Error: No Address specified",
                "kafka_message": {},
                "timestamp": str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
            }
            ))
        topic = req['topic']
        message = json.dumps(req['message']).encode()
        if 'key' in req:
            key = req['key'].encode()       # Not Required
        if 'partition' in req:
            partition = req['partition']    # 0 by default if left blank
        if 'headers' in req:
            headers = req['headers']        # Not Required
        if 'timestamp_ms' in req:
            timestamp_ms = req['timestamp_ms']  # Timestamp can be auto-generated.

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

    def getMessage(self, request):
        req = request.json
        must_haves = ['address', 'topic', 'offset']
        for musthave_key in must_haves:
            if musthave_key not in req:
                return jsonify({
                    'code': 110402,
                    'message': "You don't have " + musthave_key + " in your request."
                })
        topic = req['topic']
        address = req['address']
        offset = req['offset']
        partition = req['partition'] if 'partition' in req else 0
        consumer = KafkaConsumer(topic, bootstrap_servers=address)
        consumer.partitions_for_topic(topic)
        tp = TopicPartition(topic=topic, partition=0)
        consumer.seek(tp, offset)
        message = consumer.poll(
            timeout_ms=3000, max_records=1, update_offsets=False)
        if tp in message:
            message = message[tp][0]
            return jsonify({
                "code": 110400,
                "message": "success",
                "kafka_message": {
                    "partition": message.partition,
                    "offset": message.offset,
                    "timestamp": message.timestamp,
                    "key": message.key.decode() if message.key is not None else None,
                    "message": message.value.decode() if message.value is not None else None
                }
            })
        else:
            return jsonify({
                "code": 110403,
                "message": "No data found."
            })


    def receiveMessages(self, request):
        req = request.json
        must_haves = ['address', 'topic']
        for musthave_key in must_haves:
            if musthave_key not in req:
                return jsonify({
                    'code': 110402,
                    'message': "You don't have " + musthave_key + " in your request."
                })
        topic = req['topic']
        address = req['address']
        count = req['count'] if "count" in req else 1
        partition = req['partition'] if 'partition' in req else 0
        tp = TopicPartition(topic=topic, partition=0)

        # Create kafka consumer.
        consumer = KafkaConsumer(topic,
                                auto_offset_reset='earliest', bootstrap_servers=address)
        lastOffset = consumer.end_offsets([tp])[tp] - 1
        print('lastoffset',lastOffset)
        result = []
        found = 0
        for message in consumer:
            if 'message' in req and 'key' in req and req['key'] == message.key and req['message'] == json.loads(message.value.decode()):
                result.append({'offset':message.offset,'message':message.value.decode(),'key':message.key})
            elif 'message' in req and req['message'] == json.loads(message.value.decode()):
                result.append({'offset':message.offset,'message':message.value.decode(),'key':message.key})
            elif 'key' in req and req['key'] == message.key.decode():
                result.append({'offset':message.offset,'message':message.value.decode(),'key':message.key})
            elif 'message' not in req and 'key' not in req:
                result.append({'offset':message.offset,'message':message.value.decode(),'key':message.key})
            if found >= count or message.offset >= lastOffset:
                break
        return jsonify({
            "code": 110400,
            "message": "success",
            "kafka_message": result
        })
