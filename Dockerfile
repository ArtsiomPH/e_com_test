FROM python:3.11-alpine

RUN mkdir /app

WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY .. .

CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--port=8000"]