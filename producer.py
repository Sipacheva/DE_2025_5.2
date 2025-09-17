from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

users = ["alice", "bob", "carol", "dave"]

while True:
    data = {
        "sent_to_kafka": False,
        "user": random.choice(users),
        "event": "login",
        "timestamp": time.time()
    }
    producer.send("user_events5", value=data)
    print("Sent:", data)
    time.sleep(1)