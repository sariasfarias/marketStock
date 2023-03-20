release: python manage.py migrate --run-syncdb --settings=core.settings
web: gunicorn core.wsgi --log-file -