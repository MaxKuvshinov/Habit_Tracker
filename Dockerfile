FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/list/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN mkdir -p /app/staticfiles && chmod -R 755 /app/staticfiles

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
