release: python3 manage.py migrate --noinput && python3 manage.py loaddata initial_data.json --noinput
web: daphne -b 0.0.0.0 -p $PORT config.asgi:application