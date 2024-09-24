FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential

WORKDIR /app

COPY requirements.txt requirements.txt
COPY chatbot.py chatbot.py
COPY log_result.txt log_result.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "chatbot.py"]
