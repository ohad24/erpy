FROM postgres:12.1

RUN localedef -i he_IL -c -f UTF-8 -A /usr/share/locale/locale.alias he_IL.UTF-8

ENV LANG=he_IL.utf8

ENV TZ=Asia/Jerusalem

COPY src/sql/*.sql /sql/

COPY docker/postgres/init-user-db.sh /docker-entrypoint-initdb.d/init-user-db.sh