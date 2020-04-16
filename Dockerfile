FROM python:3.6.5

WORKDIR /app

COPY src .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
