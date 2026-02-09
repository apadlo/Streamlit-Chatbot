# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . ./

# Expose Streamlit port
EXPOSE 8501

# Default command
CMD ["streamlit", "run", "app.py"]

