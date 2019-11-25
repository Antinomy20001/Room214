python manage.py migrate --no-input &&
echo "from core.models import User; User.objects.create_superuser('admin', 'pass')" | python manage.py shell &&
exec supervisord -c /app/deploy/supervisord.conf