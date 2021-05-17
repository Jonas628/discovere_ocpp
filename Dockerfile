FROM python:3.7-alpine

# RUN apt-get update && apt-get -y install python

RUN pip install django
RUN pip install channels
RUN pip install asyncio websockets ocpp
RUN pip install psycopg2

ADD . /Central_System
#COPY . /opt/source-code

EXPOSE 8000

ENTRYPOINT CP_HANDLER=/Central_System/manage.py runserver
#CMD [ "python", "./Central_System/manage.py runserver" ]
#CMD [ "python", "./central_system.py" ]


#older version of dockerfile:
#FROM python:3.7-alpine

#ADD central_system.py /


#RUN pip install pathlib
#RUN pip install rest_framework
#RUN pip install date_time
#RUN pip install logging

#EXPOSE 8000

#CMD [ "python", "./central_system.py" ]
