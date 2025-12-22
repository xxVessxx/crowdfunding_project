FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install gunicorn==20.1.0

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "gunicorn", "crowdfunding.wsgi", "--bind", "0.0.0.0:8000"]
