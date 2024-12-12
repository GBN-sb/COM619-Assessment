# Use the official Python 3.12 slim image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy requirements first for caching layers
COPY k8s/requirements.txt .

# Install dependencies system-wide
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app/ /app

# Expose the port Streamlit will run on
EXPOSE 8501

# Check build envs
RUN env

# Set environment variables for Streamlit and the app
ENV STREAMLIT_SERVER_PORT=8501 \
    RUN_ENV=1

# Default command to run the Streamlit app
CMD ["streamlit", "run", "app.py"]
