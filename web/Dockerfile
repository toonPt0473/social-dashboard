FROM node:12-alpine
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
COPY ./ ./
RUN export NODE_ENV=production
RUN npm run build
EXPOSE 8080
CMD [ "npm", "start" ]