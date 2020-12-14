FROM python

WORKDIR /root

RUN ["python", "-m", "pip", "install", "--upgrade", "pip"]

COPY requirements.txt .

RUN ["pip", "install", "-r", "requirements.txt"]

COPY conf.json ./conf/
COPY uwsgi.ini .

COPY src/ .

CMD ["uwsgi", "--ini","uwsgi.ini"]
