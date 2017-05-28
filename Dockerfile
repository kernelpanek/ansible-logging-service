FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y libsasl2-dev libldap2-dev libssl-dev
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD ./logging_svc_webapp /code/