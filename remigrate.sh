rm -rf crank/migrations/
rm -f db.sqlite3
python manage.py makemigrations crank
python manage.py migrate
python crank/fixtures/pop.py
