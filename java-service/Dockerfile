# Use an OpenJDK base image
FROM openjdk:17-jdk-slim

# Set working directory inside the container
WORKDIR /app

# Copy jar file to container (replace with your actual jar filename)
COPY target/java-service-1.0-SNAPSHOT.jar app.jar

# Expose the default Spring Boot port
EXPOSE 8080

# Run the jar file
CMD ["java", "-jar", "app.jar"]

