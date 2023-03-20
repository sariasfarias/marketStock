release: python manage.py migrate --run-syncdb --settings=project.settings.production
web: gunicorn core.wsgi --log-file -