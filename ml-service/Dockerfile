FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY train.py .
COPY main.py .
RUN python train.py
CMD ["python", "main.py"]
