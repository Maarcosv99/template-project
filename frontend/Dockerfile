# base image
FROM node:lts-alpine

RUN npm install -g http-server

# set working directory
WORKDIR /frontend

ENV PATH /app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package*.json ./frontend/package.json
RUN npm install

COPY . .

EXPOSE 8080