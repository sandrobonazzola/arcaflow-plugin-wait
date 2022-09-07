FROM python:3.9

RUN mkdir /app
ADD wait_plugin.py /app
ADD test_wait_plugin.py /app
ADD requirements.txt /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN /usr/local/bin/python3 test_wait_plugin.py

VOLUME /config

ENTRYPOINT ["/usr/local/bin/python3", "/app/wait_plugin.py"]
CMD ["-f", "/config/wait.yaml"]