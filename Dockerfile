FROM python:3.7-alpine

LABEL maintainer="sean2525<madness48596@gmail.com>"

WORKDIR /app/src
COPY . /app/src

RUN set -e; \
    apk add --no-cache --virtual .build-deps \
    gcc \
    make \
    musl-dev \
    libc-dev \
    libffi-dev \
    openssl-dev \
    linux-headers \
    ; \
    pip3 install --no-cache-dir -U pip pipenv; \
    pipenv install --deploy --system; \
    pip3 uninstall pipenv -y; \
    apk del .build-deps;

ENV PYTHON_PROD=True

CMD ["python3", "run.py"]
