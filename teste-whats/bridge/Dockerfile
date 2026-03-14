FROM node:20-slim

ENV NODE_ENV=production

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends git \
  && rm -rf /var/lib/apt/lists/*

RUN git config --global url."https://github.com/".insteadOf ssh://git@github.com/ \
  && git config --global url."https://github.com/".insteadOf git@github.com:

COPY package.json ./
RUN npm install --omit=dev

COPY index.js ./

EXPOSE 8081

CMD ["npm", "start"]
