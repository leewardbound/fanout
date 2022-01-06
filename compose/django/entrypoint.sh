#!/bin/sh

if [ "$ENV" = "PROD" ] || [ "$ENV" = "STAGE" ] || [ "$ENV" = "DEV" ];
then
    echo "Not running in a docker-compose environment, skipping wait-for-it"
else
    echo "Waiting for dependencies to come up in the stack"
    PSQL_NAME=$(echo "${DATABASE_URL}" | sed -E "s/psql:\/\/.+:.+@(.+)\/.+/\1/g")
    if echo "${PSQL_NAME}" | grep -qE '^[-.[:alnum:]]+:[0-9]{2,5}$'; then
      timeout 10 sh -c 'until nc -w 1 -z $0; do echo "Waiting for $0 ..."; sleep 1; done' ${PSQL_NAME:-psql:5432}
    else
      echo "${PSQL_NAME} is not a valid Postgres hostname. Skipping waiting for dependencies"
    fi
fi

python3 manage.py migrate

if [ "$SERVICE" = "uwsgi" ] || [ "$SERVICE" = "runserver" ];
then
  python3 manage.py collectstatic --noinput || true
fi

exec "$@"
