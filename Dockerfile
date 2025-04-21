FROM python:3.11.4-slim-bullseye

#environment variables

#this varibale right here will tell python intrepreter to not buffer the output.....makes the error go to log in case the container shuts down we can go to the log to check where the error has occured
ENV PYTHONUNBUFFERED=1 

# and this variable will be telling the python interpreter to not write .pyc files on the import of a module ( search what are .pyc files if you dont know what they are)
ENV PYTHONDONTWRITEBYTECODE=1 

# this will be the working directory for the container
WORKDIR /app 



RUN apt-get update

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./start.sh /app/start.sh
RUN chmod +x /app/start.sh

COPY . /app/