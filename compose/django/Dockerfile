ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}

ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1

# Fix for psycopg2 ssl loading error
# https://stackoverflow.com/questions/60588431/psycopg2-import-error-ssl-check-private-key-symbol-not-found
# ENV LD_PRELOAD=/lib/libssl.so

RUN apt update -yq && apt install -yq \
     binutils libproj-dev libgdal-dev libgeos-dev

RUN ln -s /usr/lib/libproj.so.19 /usr/lib/libproj.so \
    && ln -s /usr/lib/libgeos_c.so.1 /usr/lib/libgeos_c.so


RUN pip install --no-cache-dir --upgrade pipenv pip \
    && mkdir /app

WORKDIR /app

ADD Pipfile Pipfile.lock /app/

RUN pipenv install --deploy --system

COPY compose/django/*.sh /
RUN chmod +x /*.sh

ENTRYPOINT ["/entrypoint.sh"]
