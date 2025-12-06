FROM python:3.11.9-slim

WORKDIR /app1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app1

EXPOSE 8000

CMD ["uvicorn", "app1:app", "--host", "0.0.0.0", "--port", "8000"]
