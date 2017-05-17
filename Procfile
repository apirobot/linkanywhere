web: newrelic-admin run-program gunicorn --pythonpath="$PWD/linkanywhere" wsgi:application
worker: python manage.py rqworker default
