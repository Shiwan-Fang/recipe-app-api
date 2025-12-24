
# set a basic image, alipine is a lightweight linux distribution
FROM python:3.9-alpine3.13 
# the author of this dockerfile
LABEL maintainer="qqlove" 

# ensures that python output is sent straight to terminal without being buffered
ENV PYTHONUNBUFFERED=1 

# copy the requirements file to the container
COPY ./requirements.txt /tmp/requirements.txt 
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
# set the default working directory inside the container
WORKDIR /app 
# expose port 8000 for the Django development server
EXPOSE 8000 

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# add the virtualenv to the PATH
ENV PATH="/py/bin:$PATH" 

USER django-user