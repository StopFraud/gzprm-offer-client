FROM python:3

ADD gzprm-offer-client.py /

RUN pip install --upgrade pip && \
    pip install pika requests colorama

CMD [ "python", "./gzprm-offer-client.py"]
