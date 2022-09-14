FROM python:3-alpine
RUN pip install flask zermeloapi requests
WORKDIR /script
ENTRYPOINT [ "python" ,"./run.py"]
HEALTHCHECK --interval=10s --timeout=10s --start-period=5s\
    CMD python3 healthcheck.py
COPY ./files /script/
RUN cd /script
RUN chmod 777 ./*
