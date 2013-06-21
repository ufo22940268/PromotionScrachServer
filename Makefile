server:
	python server.py

scratch-data:
	python main.py normal

scratch-test-data:
	python main.py test

update-test-data:
	python main.py update-test

replace-specific-data:
	python main.py replace-specific

save:
	echo "success!"

db:
	python db.py

print-db:
	sqlite3 test_content.db "select * from bank"

print-city:
	sqlite3 test_content.db "select * from city"

clear-db:
	sqlite3 test_content.db "delete from bank"

print-name:
	sqlite3 test_content.db "select * from name"

create-db:
	python db.py create-db

.PHONY: test
test:
	python test.py

unit-test:
	python unit_test.py

#.DEFAULT_GOAL := test
.DEFAULT_GOAL := scratch-test-data
