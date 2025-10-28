Run: python -m venv .venv; source .venv/bin/activate; pip install -r requirements.txt; cp .env.example .env; python manage.py migrate; python manage.py createsuperuser; python manage.py runserver
