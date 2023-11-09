FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8004

CMD uvicorn app.main:app --reload --port 8002