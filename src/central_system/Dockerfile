FROM python:3.7-alpine

ADD central_system.py /

RUN pip install asyncio websockets ocpp

EXPOSE 8000

CMD [ "python", "./central_system.py" ]
