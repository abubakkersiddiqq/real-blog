FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Match this to your CMD port
EXPOSE 8000 

# No --reload, and host must be 0.0.0.0
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]