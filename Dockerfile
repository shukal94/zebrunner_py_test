FROM jenkins:latest
USER root
RUN mkdir /framework
WORKDIR /framework
COPY requirements.txt /frmaework
RUN pwd
RUN ls -la
RUN apt-get update
RUN apt-get install -y python3-pip
EXPOSE 8080:8080
