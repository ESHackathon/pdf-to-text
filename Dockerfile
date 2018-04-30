FROM node:9.11

RUN apt-get update -y


RUN apt-get install -y libfreetype6-dev libmotif-dev
RUN wget https://xpdfreader-dl.s3.amazonaws.com/old/xpdf-3.03.tar.gz  # now 3.03 is current
RUN tar xzpf xpdf-3.03.tar.gz
WORKDIR "xpdf-3.03"
RUN ./configure --with-freetype2-library=/usr/lib/x86_64-linux-gnu \
    --with-freetype2-includes=/usr/include/freetype2 \
    --with-Xm-library=/usr/lib \
    --with-Xm-includes=/usr/include/Xm
RUN make
RUN make install

WORKDIR /usr/src/app

RUN apt-get install -y python-pip python-dev build-essential

COPY package*.json ./

RUN npm install

# Bundle app source
COPY . .

EXPOSE 80
CMD [ "npm", "start" ]