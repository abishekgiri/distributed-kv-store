FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the KV node code into the image
COPY kvnode ./kvnode

# Expose the port (optional, for documentation)
EXPOSE 8000

# Run the FastAPI app
CMD ["python", "-m", "kvnode.main"]
