FROM python:3.7.6

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/app .

COPY docker/flask/wait-for-it.sh .

RUN chmod +x wait-for-it.sh

COPY docker/flask/uwsgi.ini .

# uwsgi none root user
RUN chown -R www-data:www-data /app

# CMD ["./wait-for-it.sh", "postgres:5432", "--", "python", "run.py"]
CMD ["./wait-for-it.sh", "postgres:5432", "--", "uwsgi", "uwsgi.ini", "--http-keepalive"]