FROM python:3.8

WORKDIR /receipt_processor

COPY ./requirements.txt .
COPY ./app ./app
COPY ./db ./db

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "./app/main.py"]