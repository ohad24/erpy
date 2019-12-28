FROM python:3.7.5

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/app .

COPY docker/flask/wait-for-it.sh .

COPY docker/flask/uwsgi.ini .

# CMD ["./wait-for-it.sh", "postgres:5432", "--", "python", "run.py"]
CMD ["./wait-for-it.sh", "postgres:5432", "--", "uwsgi", "uwsgi.ini", "--http-keepalive"]