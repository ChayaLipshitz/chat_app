# set base image (host OS)
FROM python:3.9-slim as builder
# set the working directory in the container

# Enviroment variables
ENV ROOM_FILES_PATH "rooms/"
ENV USERS_PATH "users.csv"
ENV FLASK_ENV development

FROM builder as build1
RUN update-ca-certificates
WORKDIR /code
# copy the dependencies file to the working directory

VOLUME my-volume:/code

FROM builder as build2
COPY requirements.txt .

# install dependencies
RUN mkdir /data  && \
    pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# command to run on container start
CMD [ "python", "./chatApp.py" ]

# Helth check
HEALTHCHECK CMD ["curl", "-f", "http://localhost:5000/health"] INTERVAL=10s TIMEOUT=3s

# copy the content of the local src directory to the working directory
COPY . .
