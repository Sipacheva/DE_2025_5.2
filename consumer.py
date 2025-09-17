from kafka import KafkaConsumer
import psycopg2
import json

consumer = KafkaConsumer(
    "user_events5",
    bootstrap_servers="localhost:9092",
    group_id="user-logins-consumer5",
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

conn = psycopg2.connect(
    dbname="test_db", user="admin", password="admin", host="localhost", port=5432
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_logins (
    sent_to_kafka BOOLEAN,
    id SERIAL PRIMARY KEY,
    username TEXT,
    event_type TEXT,
    event_time TIMESTAMP
)
""")
conn.commit()

for message in consumer:
    data = message.value
    print("Received:", data)

    cursor.execute(
        "INSERT INTO user_logins (sent_to_kafka, username, event_type, event_time) VALUES (%s, %s, %s, to_timestamp(%s))",
        (data["sent_to_kafka"], data["user"], data["event"], data["timestamp"])
    )
    conn.commit()