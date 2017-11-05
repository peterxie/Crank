rm -rf crank/migrations/
rm -f db.sqlite3
python manage.py makemigrations crank
python manage.py migrate
python manage.py loaddata crank/fixtures/init.json
