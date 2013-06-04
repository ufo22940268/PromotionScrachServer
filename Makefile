all:
	python main.py

server:
	python server.py

save:
	echo "success!"

db:
	python db.py

print-db:
	sqlite3 content.db "select * from bank"

clear-db:
	sqlite3 content.db "delete from bank"
