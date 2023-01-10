python3 manage.py collectstatic --noinput
python3 manage.py migrate
python3 manage.py filldatabase
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'a@a.ru', 'admin')" | python3 manage.py shell
# pip3 install gunicorn
# gunicorn foodgram_backend.wsgi:application --bind 0:8000
python3 manage.py runserver 0:8000