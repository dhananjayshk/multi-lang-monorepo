# Stage 1: Build the Go application
FROM golang:1.22.2 AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy Go module files
COPY go.mod ./

# Download dependencies
RUN go mod download

# Copy the source code
COPY . .

# Build the Go binary
RUN go build -o main .

# Stage 2: Create a minimal image
FROM debian:bullseye-slim

# Set working directory
WORKDIR /app

# Copy the binary from the builder stage
COPY --from=builder /app/main .

# Copy any config or templates if required
# COPY ./config ./config

# Expose port (change this to your actual port if needed)
EXPOSE 8080

# Command to run the application
CMD ["./main"]

