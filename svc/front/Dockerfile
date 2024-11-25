# Stage 1: Build the React application
FROM node:18-alpine AS builder

# Set working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire project directory into the container
COPY . .

# Build the React application for production
RUN npm run build

# Stage 2: Serve the application using a lightweight web server
FROM nginx:alpine

# Copy the build output from the previous stage to Nginx's web directory
COPY --from=builder /app/build /usr/share/nginx/html

# Expose port 80 to the outside world
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
