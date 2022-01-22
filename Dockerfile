# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.8.5

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3","webApp/manage.py","runserver","0.0.0.0:8000"]

