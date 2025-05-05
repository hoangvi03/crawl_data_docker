FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    gcc build-essential libssl-dev libffi-dev libxml2-dev \
    libxslt1-dev libjpeg-dev zlib1g-dev curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install playwright && playwright install --with-deps

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /code/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
