# DE_2025_5.2
# Перенос данных из PostgreSQL в ClickHouse без дубликатов

## Реализован следующий сценарий:
:heavy_check_mark: В БД PostgreSQL создана таблица user_logins, в которую добавлено поле sent_to_kafka со значением по умолчанию FALSE

:heavy_check_mark: Продюсер (producer_pg_to_kafka.py) отправляет в Kafka только те строки, у которых поле sent_to_kafka = FALSE

:heavy_check_mark: После отправки данных значение поля sent_to_kafka меняется на TRUE

:heavy_check_mark: Консьюмер получает данные из Kafka и сохраняет в ClickHouse в таблицу user_logins 

:heavy_check_mark: При загружке новых данных в таблицу user_logins БД PostgreSQL процесс повторяется, т.к. у них sent_to_kafka = FALSE

:heavy_check_mark: После загрузки осуществляется проверка того, что все строки перенесли из PostgreSQL в ClickHouse (количество строк в обеих БД совпадает)

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

### Подготовительные шаги:
* Запустить образ в терминале проекта при помощи команды `docker-compose up -d`
* Запустить produсer.py в терминале проекта `python producer.py`
  После того как необходимое количество данных будет передано, остановить producer командой `ctrl-c`
  

* Запустить consumer.py в терминале проекта `python consumer.py`, остановить producer командой `ctrl-c`
   
* На данном этапе подготовительные шага закончены, в БД test_db таблица user_logins заплонена строками, у которых поле sent_to_kafka = FALSE. Проверить можно, выполнив запрос в DBeaver `select * from user_logins`
  
  
### Перенос данных из PostgreSQL в ClickHouse:
* Запустить producer_pg_to_kafka.py в терминале проекта `producer_pg_to_kafka.py`
  
* Запустить consumer_to_clickhouse.py в терминале проекта `python consumer_to_clickhouse.py`
  




Проверки
Ошибка
<img width="692" height="104" alt="image" src="https://github.com/user-attachments/assets/7576c3a8-100a-45e8-aa11-f24143ec2f49" />
