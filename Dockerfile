FROM python:3.9-slim

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app_user

WORKDIR /code

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create .streamlit directory with proper permissions
RUN mkdir -p /home/app_user/.streamlit && \
    chown -R app_user:app_user /home/app_user/.streamlit && \
    chown -R app_user:app_user /code

# Switch to non-root user
USER app_user

# Set environment variables
ENV HOME=/home/app_user
ENV STREAMLIT_SERVER_PORT=7860
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

EXPOSE 7860

CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0", "--server.headless=true", "--server.fileWatcherType=none"]