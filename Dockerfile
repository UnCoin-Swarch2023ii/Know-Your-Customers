# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Load environment variables from the .env file
RUN ["python", "-c", "import dotenv; dotenv.load_dotenv()"]

# Expose the port your app runs on
EXPOSE 3000

# Define environment variable for Flask to run in production mode
ENV FLASK_ENV=development

# Run app.py when the container launches
CMD ["bash", "-c", "python app.py & python helpers/imageConsumer.py"]
