# Dockerfile
FROM python:3.9.17-bookwork

ENV PYTHONUNBUFFERED TRUE
ENV APP_HOME /back_end¨
WORKDIR $APP_HOME
COPY . ./

RUN pip install --no-cache-dir --upgrade 
RUN pip install --no-cache-dir -r requirements.txt 

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app]