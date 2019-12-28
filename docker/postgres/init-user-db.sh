#!/usr/bin/env bash

psql -f /sql/001_DB_Infrastructure.sql \
    -v postgres_db=$POSTGRES_DB \
    -v postgres_password="'$POSTGRES_PASSWORD'" \
    -v lang="'$LANG'" \
    -v tz="'$TZ'"
psql -d $POSTGRES_DB -U erpy -q -f /sql/002_Schema.sql
psql -d $POSTGRES_DB -U erpy -q -f /sql/003_Tables.sql
psql -d $POSTGRES_DB -U erpy -q -f /sql/004_Functions.sql
psql -d $POSTGRES_DB -U erpy -q -f /sql/005_Views.sql
psql -d $POSTGRES_DB -U erpy -q -f /sql/009_Data.sql