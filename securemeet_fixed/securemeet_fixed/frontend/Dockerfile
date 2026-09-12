# ── Build stage ───────────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install --legacy-peer-deps

COPY . .
RUN npm run build:prod

# ── Nginx stage ───────────────────────────────────────────────────
FROM nginx:alpine

# Copy built Angular app
COPY --from=builder /app/dist/securemeet-frontend/browser /usr/share/nginx/html

# Angular routing support — all routes → index.html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s \
  CMD wget -q --spider http://localhost:80 || exit 1

CMD ["nginx", "-g", "daemon off;"]
