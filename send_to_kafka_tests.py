import clickhouse_connect
import psycopg2

conn = psycopg2.connect(
    dbname="test_db", user="admin", password="admin", host="localhost", port=5432
)
cursor = conn.cursor()

client = clickhouse_connect.get_client(host='localhost', port=8123, username='user', password='strongpassword')

# Сравнение количества строк в таблице user_logins в базах PostgreSQL и ClickHouse
cursor.execute("SELECT COUNT(*) FROM user_logins")
posrgreSQL_count = cursor.fetchone()[0]

clickhouse_count = client.command("SELECT COUNT(*) FROM user_logins")

if posrgreSQL_count == clickhouse_count:
    print("Количество строк в таблице user_logins в базах PostgreSQL и ClickHouse одинаковое")
else:
    print(f"Количество строк отличается: {posrgreSQL_count} vs {clickhouse_count}")

# Проверка того, что в таблице user_logins в PostgreSQL не осталось строк, которые нужно переносить в ClickHouse
cursor.execute("SELECT COUNT(*) FROM user_logins WHERE sent_to_kafka = false")
posrgreSQL_sent_to_kafka_false_count = cursor.fetchone()[0]

if posrgreSQL_sent_to_kafka_false_count == 0:
    print("В таблице user_logins в PostgreSQL не осталось строк, которые нужно переносить в ClickHouse")
else:
    print(f"В таблице user_logins в PostgreSQL {posrgreSQL_sent_to_kafka_false_count} строк, которые нужно переносить в ClickHouse")