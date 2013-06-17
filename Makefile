server:
	python server.py

all:
	python main.py

.PHONY: test
test:
	python test.py

save:
	echo "success!"

db:
	python db.py

print-db:
	sqlite3 content.db "select * from bank"

clear-db:
	python db.py

print-name:
	sqlite3 content.db "select * from name"

.DEFAULT_GOAL := test
