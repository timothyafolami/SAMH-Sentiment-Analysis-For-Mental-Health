# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Download NLTK data
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the entrypoint script
CMD ["sh", "./entrypoint.sh"]
