#!/usr/bin/env bash

pushd /app
daphne -b 0.0.0.0 -p 8000 asgi:application
