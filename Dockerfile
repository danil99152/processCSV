# Use latest Python 3.11 image as the base image
FROM python:3.11

# Copy the application code to the working directory (root)
COPY core core

# Install dependencies from requirements.txt
RUN pip install -r core/requirements.txt

# Expose port 5000
EXPOSE 5000

# Run the app
CMD python core/main.py

# Build image command
# docker build -t processcsv .

# Run container command
# docker run -p 5000:5000 --name processcsv processcsv
