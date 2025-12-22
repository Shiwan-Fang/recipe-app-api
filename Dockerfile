
# set a basic image, alipine is a lightweight linux distribution
FROM python:3.9-alpine3.13 
# the author of this dockerfile
LABEL maintainer="qqlove" 

# ensures that python output is sent straight to terminal without being buffered
ENV PYTHONUNBUFFERED=1 

# copy the requirements file to the container
COPY ./requirements.txt /tmp/requirements.txt 
COPY ./app /app
# set the default working directory inside the container
WORKDIR /app 
# expose port 8000 for the Django development server
EXPOSE 8000 

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# add the virtualenv to the PATH
ENV PATH="/py/bin:$PATH" 

USER django-user