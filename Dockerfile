FROM docker.io/library/python:3.11-alpine

RUN addgroup no-name && \
    adduser -G no-name -h /home/no-name -s /bin/sh -D no-name

WORKDIR /usr/src/app

RUN chown -R no-name:no-name /usr/src/app

COPY --chown=no-name:no-name ./requirements.txt ./requirements.txt

RUN apk add --no-cache --virtual .build-deps gcc=~12.2.1_git20220924-r10 musl-dev=~1.2.4-r1 \
    && pip3 install --no-cache-dir --upgrade pip==23.2.1 \
    && pip3 install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

COPY --chown=no-name:no-name ./ /usr/src/app/

USER no-name

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "curl" , "-f", "http://localhost:8080/" ]

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080" ]
