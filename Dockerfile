# # Use the official lightweight Python image.
# # https://hub.docker.com/_/python
# FROM python:3.8-slim

# # Copy local code to the container image.
# ENV APP_HOME /app
# ENV PYTHONUNBUFFERED True
# WORKDIR $APP_HOME

# # Install gcc and python3-dev
# RUN apt-get update && \
#     apt-get install -y gcc python3-dev && \
#     rm -rf /var/lib/apt/lists/*

# # Install Python dependencies and Gunicorn
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir gunicorn

# # Create a non-root user to run the application
# RUN groupadd -r app && useradd -r -g app app
# RUN chown -R app:app $APP_HOME
# USER app

# # Copy the rest of the codebase into the image
# COPY . .

# # Run the web service on container startup. Here we use the gunicorn
# # webserver, with one worker process and 8 threads.
# # For environments with multiple CPU cores, increase the number of workers
# # to be equal to the cores available in Cloud Run.
# CMD exec gunicorn --bind :$PORT --log-level info --workers 1 --threads 8 --timeout 0 app:server

#From https://towardsdatascience.com/docker-for-python-dash-r-shiny-6097c8998506

FROM python:3.9-slim-buster

LABEL maintainer "Elise Alstad"

LABEL maintainer "Meinhard Ploner <dummy@host.com>"
WORKDIR /code
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY ./ ./
EXPOSE 8050
CMD ["python", "./app.py"]