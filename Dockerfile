FROM python:3-alpine3.17

# Build-time metadata as defined at https://github.com/opencontainers/image-spec/blob/main/annotations.md
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION
LABEL     org.opencontainers.image.created=${BUILD_DATE} \
          org.opencontainers.image.url="https://github.com/angeloc/s3-pit-restore" \
          org.opencontainers.image.version=${VERSION} \
          org.opencontainers.image.revision=${VCS_REF} \
          org.opencontainers.image.vendor="angeloc" \
          org.opencontainers.image.licenses="MIT" \
          org.opencontainers.image.title="s3-pit-restore" \
          org.opencontainers.image.description="a point in time restore tool for Amazon S3."

RUN pip3 --no-cache-dir install awscli

ADD . /tmp/
WORKDIR /tmp/
RUN python3 setup.py install

ENTRYPOINT [ "s3-pit-restore" ]
CMD [ "-h" ]
