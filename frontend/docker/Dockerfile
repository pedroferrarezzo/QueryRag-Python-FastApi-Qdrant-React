FROM node:22-alpine AS build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

COPY . .

ARG VITE_API_ENDPOINT
ARG VITE_WS_CHAT_ENDPOINT

ENV VITE_API_ENDPOINT=${VITE_API_ENDPOINT}
ENV VITE_WS_CHAT_ENDPOINT=${VITE_WS_CHAT_ENDPOINT}

RUN npm run build

FROM nginx:1.27-alpine AS runtime

COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
