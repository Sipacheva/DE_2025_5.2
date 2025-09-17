# consumer_to_clickhouse.py
from kafka import KafkaConsumer
import json
import clickhouse_connect

consumer = KafkaConsumer(
    "user_events5",
    bootstrap_servers="localhost:9092",
    group_id="user-logins-consumer5",
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

client = clickhouse_connect.get_client(host='localhost', port=8123, username='user', password='strongpassword')

client.command("""
CREATE TABLE IF NOT EXISTS user_logins (
    id UInt64,
    username String,
    event_type String,
    event_time DateTime
) ENGINE = MergeTree()
ORDER BY event_time
""")

for message in consumer:
    data = message.value
    print("Received:", data)
    client.command(
        f"INSERT INTO user_logins (id, username, event_type, event_time) VALUES ('{data['id']}', '{data['user']}', '{data['event']}', toDateTime({data['timestamp']}))"
    )