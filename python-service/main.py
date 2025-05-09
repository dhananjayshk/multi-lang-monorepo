import logging

# Set up logging to a file
logging.basicConfig(filename='/app/logs/python/app.log', level=logging.INFO)

def main():
    logging.info("Python service started")
    print("Hello from Python service!")

if __name__ == "__main__":
    main()

