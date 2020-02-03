FROM node:10

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY webApp/package*.json ./

# Bundle app source
COPY . .

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install git build-essential bash-completion python3-dev vim curl wget tar mysql-server python3-pip python3-mysqldb
RUN pip3 install --upgrade pip
RUN pip3 install gtfs-realtime-bindings requests mysql

RUN cd webApp && npm install

EXPOSE 8080

