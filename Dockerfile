FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY application application

COPY wsgi.py config.py ./

EXPOSE 5000

CMD [ "python", "wsgi.py"]