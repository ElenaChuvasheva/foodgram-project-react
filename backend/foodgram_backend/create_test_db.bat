python manage.py migrate
python manage.py filldatabase
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'admin') | python manage.py shell
python manage.py runserver