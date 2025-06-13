FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8000 8501
CMD ["sh", "-c", "uvicorn backend.app:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.address 0.0.0.0 --server.port 8501"]
