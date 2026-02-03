FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy requirements dulu
COPY requirement.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Copy semua source code
COPY . .

# Expose port FastAPI
EXPOSE 8000

# Run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
