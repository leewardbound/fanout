ARG image_version=python:3.9.5-alpine3.12


#
#
# Base stage
FROM ${image_version} as base

ENV PATH=/app/.venv/bin:$PATH
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1

# Fix for psycopg2 ssl loading error
# https://stackoverflow.com/questions/60588431/psycopg2-import-error-ssl-check-private-key-symbol-not-found
ENV LD_PRELOAD=/lib/libssl.so.1.1

RUN apk add --no-cache libpq libjpeg libcurl bash libxml2-dev libxslt-dev curl-dev build-base


#
#
# Builder stage
FROM base as builder

RUN apk add --no-cache zlib-dev jpeg-dev gcc python3-dev musl-dev postgresql-dev linux-headers build-base libcurl curl-dev libressl-dev libxml2-dev libxslt-dev libffi-dev openssl

RUN pip install --no-cache-dir --upgrade pipenv pip
COPY Pipfile Pipfile.lock /app/

WORKDIR /app
RUN PIPENV_VENV_IN_PROJECT=true pipenv install --deploy

COPY fanout/ /app/fanout
COPY manage.py wsgi.py asgi.py /app/

# Needed for fixtures to run in e2e tests
#COPY fixtures/ /app/fixtures

RUN SECRET_KEY=_ignore_during_build_ pipenv run python manage.py collectstatic --no-input

COPY ./compose/django/*.sh /
RUN chmod +x /*.sh


#
#
# Release stage
FROM base as release

COPY --from=builder /app /app
COPY --from=builder /*.sh /

WORKDIR /app
ENTRYPOINT ["/entrypoint.sh"]

#
#
# Test stage

FROM release as test

# copy in test dependencies
COPY pytest.ini pyproject.toml /app/
#COPY fixtures/ /app/fixtures
#
#
# This make release the default stage
FROM release
