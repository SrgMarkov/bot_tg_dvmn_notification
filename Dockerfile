FROM python:3.10

RUN mkdir -p /opt/app/
COPY requirements.txt /opt/app/requirements.txt

WORKDIR /opt/app
RUN pip install -r requirements.txt
COPY . /opt/app

CMD ["python3", "main.py"]