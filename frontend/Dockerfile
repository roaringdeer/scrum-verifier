# base image
FROM node:10.15.0
 
# set working directory
# RUN mkdir /usr/src/app
RUN npm install -g @vue/cli

WORKDIR /frontend
COPY . .
RUN npm install
# add `/usr/src/app/node_modules/.bin` to $PATH
# ENV PATH /node_modules/.bin:$PATH
 
# install and cache app dependencies
# COPY package.json .
# COPY package-lock.json .
# COPY ./public /frontend
# COPY ./src /frontend
# COPY Dockerfile /frontend

RUN npm install --save axios vue-router@next vue-loader-v16 jwt-decode primevue chart.js vuedraggable@next @fullcalendar/core @fullcalendar/daygrid @fullcalendar/timegrid @fullcalendar/interaction @fullcalendar/list


# start app
# CMD ["npm", "run", "serve"]