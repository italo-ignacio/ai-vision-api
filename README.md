pip install -r requirements.txt

alembic revision --autogenerate -m ""

alembic upgrade head

py run.py
