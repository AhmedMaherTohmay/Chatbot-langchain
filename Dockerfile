# Use an official Python runtime as a parent image
FROM python:3.10-slim

#Copy the current folder structure and content to docker folder
COPY . /usr/Chatbot

#Expose the port within docker 
EXPOSE 5000

#Set current working directory
WORKDIR /usr/Chatbot

#Install the required libraries
RUN pip install --no-cache-dir -r requirements.txt

#container start up command
CMD python3 app.py