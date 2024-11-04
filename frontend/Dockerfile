FROM node:alpine

#copy source 
COPY package.json package-lock.json /app/

# Install deps
RUN cd /app && npm install --legacy-peer-deps

WORKDIR /app

COPY . /app

# Build 
RUN npm run build --legacy-peer-deps

ENTRYPOINT [ "npm", "run", "start" ]
