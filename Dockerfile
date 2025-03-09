# Use Python 3.11 as the base image
FROM python:3.11

# Set working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .  

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1
# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--debug"]