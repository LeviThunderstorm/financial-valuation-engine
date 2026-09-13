# Stage 1: Build Assets
FROM nginx:1.25-alpine AS builder

WORKDIR /usr/share/nginx/html
COPY ./src .

# Stage 2: Production Nginx Server
FROM nginx:1.25-alpine AS runner

# Remove default configuration & copy custom reverse proxy setup
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy static assets from builder stage
COPY --from=builder /usr/share/nginx/html /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]