from python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED True

ENV PORT 8080
EXPOSE $PORT

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . ./

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app