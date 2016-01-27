FROM python:2.7
MAINTAINER Alex Etling <alex@gc.io>

ADD . /zookeeper_dashboard

RUN pip install -r /zookeeper_dashboard/requirements.txt

CMD cd /zookeeper_dashboard; python manage.py runserver
