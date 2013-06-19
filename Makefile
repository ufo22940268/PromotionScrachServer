server:
	python server.py

scratch-data:
	python main.py


save:
	echo "success!"

db:
	python db.py

print-db:
	sqlite3 content.db "select * from bank"

print-city:
	sqlite3 content.db "select * from city"

clear-db:
	sqlite3 content.db "delete from bank"

print-name:
	sqlite3 content.db "select * from name"

create-db:
	python db.py create-db

.PHONY: test
test:
	python test.py

unit-test:
	python unit_test.py

.DEFAULT_GOAL := test
