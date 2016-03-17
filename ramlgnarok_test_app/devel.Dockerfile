FROM python:3.5

MAINTAINER Pawel Kucmus <pkucmus@gmail.com>

ADD ramlgnarok_test_app/requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=service.local_settings

ADD ramlgnarok_test_app /run/service
WORKDIR /run/service

ADD . /run/ramlgnarok
RUN pip install -e /run/ramlgnarok

EXPOSE 8000

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
