FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY wsgi.py .
COPY config.py .
COPY application application

EXPOSE 5000

CMD [ "python", "wsgi.py"]