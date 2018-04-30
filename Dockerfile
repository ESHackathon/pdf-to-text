FROM node:9.11

WORKDIR /usr/src/app

RUN apt-get update -y
RUN apt-get install -y poppler-utils
RUN apt-get install -y python-pip python-dev build-essential

COPY package*.json ./

RUN npm install
# If you are building your code for production
# RUN npm install --only=production

# Bundle app source
COPY . .

EXPOSE 80
CMD [ "npm", "start" ]