# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7-slim-buster

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN apt-get update && apt-get install gcc -y && apt-get clean
RUN pip install --no-cache-dir -r requirements.txt

ADD https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 /app/cloud_sql_proxy
RUN chmod +x ./cloud_sql_proxy

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD ./cloud_sql_proxy -instances=dataritma-vf-myaml:europe-west3:vf-db=tcp:3306 & exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
