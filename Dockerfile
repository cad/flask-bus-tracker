FROM python:2.7-alpine

# RUN apk add --update \
#     python \
#     python-dev \
#     py-pip \
#     build-base \
#   && pip install virtualenv \
#   && rm -rf /var/cache/apk/*

#RUN apk add --update build-base
RUN apk add --update gcc libffi-dev python-dev musl-dev mariadb-dev

COPY . /srv
RUN pip install -r /srv/requirements.pip && pip install gunicorn mysql-python eventlet pytest pytest-faker
RUN rm -rf /srv/tests/*.pyc /srv/tests/__pycache__
EXPOSE 4000
WORKDIR /srv
CMD ["gunicorn", "-k eventlet", "-w 4", "-b 0.0.0.0:4000", "api.wsgi:app", "--log-level=debug", "-t=120"]
