FROM python:2.7
MAINTAINER Alex Etling <alex@gc.io>

ADD . /zookeeper_dashboard

RUN pip install -r /zookeeper_dashboard/requirements.txt

CMD cd /zookeeper_dashboard; gunicorn -b '0.0.0.0:80' -w 4 zookeeper_dashboard.wsgi:application
