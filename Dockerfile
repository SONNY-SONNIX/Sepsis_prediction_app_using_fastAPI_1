# FROM python:3.9

# WORKDIR /code

# COPY ./requirements.txt /code/requirements.txt

# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY . .

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]


# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the  xgb_model.joblib files to the container
COPY xgb_model.joblib .

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port that the FastAPI application will run on
EXPOSE 7860

# Command to run the FastAPI application when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]


