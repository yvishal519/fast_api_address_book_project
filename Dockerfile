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

# Define build arguments for database configuration
ARG DATABASE
ARG PORT
ARG USER
ARG PASSWORD
ARG HOST
ARG SCHEMA

# Update environment_variables.conf with the provided database configuration
RUN echo "[PSQL_DB]" > configurations/environment_variables.conf
RUN echo "database = $DATABASE" >> configurations/environment_variables.conf
RUN echo "port = $PORT" >> configurations/environment_variables.conf
RUN echo "user = $USER" >> configurations/environment_variables.conf
RUN echo "password = $PASSWORD" >> configurations/environment_variables.conf
RUN echo "host = $HOST" >> configurations/environment_variables.conf
RUN echo "schema = $SCHEMA" >> configurations/environment_variables.conf

# Command to run the Python application
CMD ["python", "src/baker_hughes_extractor/main.py"]

# command to build docker image
# sudo docker build --build-arg DATABASE=postgres --build-arg PORT=5432 --build-arg USER=new_username --build-arg PASSWORD=Abcdef123 --build-arg HOST=localhost --build-arg SCHEMA=web_scrapes -t my-python-app .

# command to run docker image
# sudo docker run my-python-app