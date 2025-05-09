# Step 1: Build the Rust application
FROM rust:1.68 as builder

# Set the working directory
WORKDIR /app

# Copy the Rust source code to the container
COPY . .

# Build the Rust application in release mode
RUN cargo build --release

# Step 2: Create the final image with the compiled binary
FROM debian:bullseye-slim

# Set the working directory
WORKDIR /app

# Copy the compiled binary from the builder stage
COPY --from=builder /app/target/release/rust_service .

# Expose the necessary port
EXPOSE 8080

# Run the Rust application when the container starts
CMD ["./rust_service"]

