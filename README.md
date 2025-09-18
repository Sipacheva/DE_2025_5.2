# DE_2025_5.2
# Перенос данных из PostgreSQL в ClickHouse без дубликатов

## Реализован следующий сценарий:
:heavy_check_mark: В БД PostgreSQL создана таблица user_logins, в которую добавлено поле sent_to_kafka со значением по умолчанию FALSE

:heavy_check_mark: Продюсер (producer_pg_to_kafka.py) отправляет в Kafka только те строки, у которых поле sent_to_kafka = FALSE

:heavy_check_mark: После отправки данных значение поля sent_to_kafka меняется на TRUE

:heavy_check_mark: Консьюмер получает данные из Kafka и сохраняет в ClickHouse в таблицу user_logins 

:heavy_check_mark: При загружке новых данных в таблицу user_logins БД PostgreSQL процесс повторяется, т.к. у них sent_to_kafka = FALSE

:heavy_check_mark: После загрузки осуществляется проверка того, что все строки перенесли из PostgreSQL в ClickHouse (количество строк в обеих БД совпадает, в таблице user_logins в PostgreSQL нет строк, которые нужно переносить в ClickHouse)

## Стек технологий:
<img width="50" height="50" alt="kafka" src="https://github.com/user-attachments/assets/973d959b-3834-4f48-8c3b-34b66ccc9a2c" />
<img width="50" height="50" alt="postgresql" src="https://github.com/user-attachments/assets/783c27fd-bfdf-41ae-8e02-6df185a0f916" />
<img width="50" height="50" alt="clickhouse" src="https://github.com/user-attachments/assets/5be9e2bd-212f-44a9-85af-088783c03121" />
<img width="50" height="50" alt="PyCharm" src="https://github.com/user-attachments/assets/1c692a21-b80b-442e-9426-0475cd7759cc" />
<img width="50" height="50" alt="python" src="https://github.com/user-attachments/assets/bfed65a3-6e12-4f49-bb29-975d206a1f93" />
<img width="50" height="50" alt="github" src="https://github.com/user-attachments/assets/dadd861d-a4a6-4fcc-a072-024f7097d943" />
<img width="50" height="50" alt="docker" src="https://github.com/user-attachments/assets/8d374f34-f79d-4e57-b49c-16a4428c18c8" />
<img width="50" height="50" alt="dbeaver" src="https://github.com/user-attachments/assets/5bb33bf3-e16e-4e4a-bf83-dd389981c365" />

## Как запустить:

### 1. Подготовительные шаги:
* Запустить образ в терминале проекта при помощи команды `docker-compose up -d`
* Запустить produсer.py в терминале проекта `python producer.py`
  После того как необходимое количество данных будет передано, остановить producer командой `ctrl-c`
  <img width="799" height="117" alt="image" src="https://github.com/user-attachments/assets/715cee30-3380-46d7-8c04-69f095738bbd" />
* Запустить consumer.py в терминале проекта `python consumer.py`, остановить producer командой `ctrl-c`
   <img width="828" height="136" alt="image" src="https://github.com/user-attachments/assets/f8007840-c2ee-4c03-a2c1-d2208ff86847" />
* На данном этапе подготовительные шага закончены, в БД test_db таблица user_logins заплонена строками, у которых поле sent_to_kafka = FALSE. Проверить можно, выполнив запрос в DBeaver `select * from user_logins`
  
### 2. Перенос данных из PostgreSQL в ClickHouse:
* Запустить producer_pg_to_kafka.py в терминале проекта `producer_pg_to_kafka.py`. Данные, у которых sent_to_kafka = FALSE, отправятся в Kafka, после этого признак sent_to_kafka изменится на TRUE, чтобы данные не дублировались.
  <img width="796" height="106" alt="image" src="https://github.com/user-attachments/assets/9e837eeb-fb7c-485e-a249-cfc57f81d846" />

* Запустить consumer_to_clickhouse.py в терминале проекта `python consumer_to_clickhouse.py`. В ClickHouse будет создана таблица с данными, переданными producer_pg_to_kafka.py. Либо, если таблица уже существует, в нее добавятся новые строки.
  <img width="796" height="106" alt="image" src="https://github.com/user-attachments/assets/e1adff52-5393-4177-8c74-8d2c1781432e" />
* Можно проверить количество строк в таблице user_logins в ClickHouse вручную, выполнив запрос `SELECT COUNT() FROM user_logins`
* Чтобы не проверять вручную, нужно запустить send_to_kafka_tests.py, который проверит:
  - Сравнение количества строк в таблице user_logins в базах PostgreSQL и ClickHouse
  - В таблице user_logins в PostgreSQL не осталось строк, которые нужно переносить в ClickHouse
  Если перенос успешен, то выдается сообщение:
  <img width="745" height="56" alt="image" src="https://github.com/user-attachments/assets/46651d01-b7bb-4905-8114-ae07559f0ce8" />

  Если не все строки перенесены, и/или количество строк в таблицах разное, выдаются сообщения `Количество строк отличается`, `В таблице user_logins в PostgreSQL n строк, которые нужно переносить в ClickHouse`.
  Например, сразу оба сообщения:
  <img width="692" height="104" alt="image" src="https://github.com/user-attachments/assets/7576c3a8-100a-45e8-aa11-f24143ec2f49" />

### 3. Проверим, что при повторном переносе из PostgreSQL в ClickHouse данные не дублируются:
* Запустить produсer.py, а затем consumer.py, добавив несколько строк в таблицу user_logins в PostgreSQL.
* Запустить send_to_kafka_tests.py, а затем consumer_to_clickhouse.py, добавив строки в таблицу user_logins в ClickHouse.
* Запустить send_to_kafka_tests.py, проверив, что количество строк в таблицах в обеих БД совпадает, т.е. данные не задублировались (или проверить вручную).

## Также пример переноса из PostgreSQL в ClickHouse можно посмотреть на видео:

https://github.com/user-attachments/assets/a01596fb-f9cb-4c36-9815-e87945852189

