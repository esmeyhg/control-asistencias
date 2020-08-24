FROM python:3.6

RUN mkdir /dependencias

COPY requirements.txt /dependencias

RUN pip3 install -r /dependencias/requirements.txt

ENV SECRET_KEY_ESTATICO=""
ENV DB_USER_ESTATICO=""
ENV DB_NAME_ESTATICO=""
ENV DB_PASSWORD_ESTATICO=""
ENV DB_HOST_ESTATICO=""
ENV DB_PORT_ESTATICO=3306
ENV PATH_PREFIX=""

RUN mkdir /code
RUN mkdir /start
RUN mkdir /monitor

COPY ./run.sh /start
RUN chmod 751 /start/run.sh
COPY ./monitor.py /monitor

WORKDIR /code

RUN useradd -s /bin/bash restringido

RUN chown -R restringido /code

CMD /start/run.sh