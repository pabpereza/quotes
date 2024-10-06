FROM python:3.11-slim

WORKDIR /app

RUN apt update && apt install -y libpq-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["fastapi", "run", "app/main.py", "--port","80"]
