#!/bin/sh

# Apply database migrations
poetry run python manage.py migrate

# Populate OMW words (custom command)
poetry run python manage.py populate_omw_words