FROM python:3.7-alpine

COPY mew-sampler.py mew-logger.py startup.sh /tmp/

RUN chmod +x /tmp/* && \
    mv /tmp/* /usr/sbin && \
    pip3 install requests
CMD /usr/sbin/startup.sh
