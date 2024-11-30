# Base image Python 3.12 (Debian)
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app/process_images.py /app/
COPY ./app/requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN apt-get update
RUN apt-get install -y libimage-exiftool-perl

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Run the Python script when the container launches
CMD ["python", "process_images.py"]

# Run this commnad to do tests only, comment prevous CMD command
# CMD ["tail", "-f", "/dev/null"]