FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --timeout 1000 --retries 5 -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]