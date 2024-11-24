# Use the official Python 3.11 slim image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install pip and setuptools, then install the dependencies
RUN pip install --upgrade pip setuptools \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the default Streamlit port
EXPOSE 8501

# Set the environment variable for Streamlit to run in headless mode
ENV STREAMLIT_SERVER_HEADLESS=true

# Command to run the Streamlit application
CMD ["streamlit", "run", "app.py"]