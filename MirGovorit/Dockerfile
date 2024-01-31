FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1
WORKDIR /MirGovorit
RUN apt-get update \
    && apt-get install -y libpq-dev python3-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /MirGovorit/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /MirGovorit/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]