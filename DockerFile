# Use official Python image
FROM python:3.9

# Working directory
WORKDIR /app

# Copy necessary files
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose port for MLflow UI
EXPOSE 5000

# Run the script
CMD ["python", "script.py"]

