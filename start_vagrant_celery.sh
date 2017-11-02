#!/bin/bash

celery -A workers.vagranttasks worker -b redis://127.0.0.1/1 --loglevel=DEBUG  -n vagrant@%h --concurrency=3
