FROM node:25-alpine

# Build with repository root as context:
# docker build -f mcp-app-server/Dockerfile -t drawio-mcp-app-server:v1 .
WORKDIR /app

COPY mcp-app-server/package*.json ./mcp-app-server/
RUN npm --prefix mcp-app-server install

COPY mcp-app-server ./mcp-app-server
COPY shared ./shared
COPY shape-search ./shape-search

WORKDIR /app/mcp-app-server
ENV PORT=3000

EXPOSE 3000
CMD ["npm", "start"]
