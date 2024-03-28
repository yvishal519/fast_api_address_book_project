# Use the official Python image as the base image
FROM python:3.10.13

# Set the working directory in the container
WORKDIR /code

# Copy the entire project directory into the container
COPY . /code

# Set the PYTHONPATH environment variable to include the root directory of your project
ENV PYTHONPATH "${PYTHONPATH}:/code"

# Install dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the Python application
CMD ["python", "app.py"]