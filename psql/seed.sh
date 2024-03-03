#!/bin/bash

# init db dir
su -l postgres -c "/usr/local/bin/initdb -D /var/lib/postgresql/data"

# add so we can access db from adminer docker or anywhere we need
echo "host all all all trust" >> /var/lib/postgresql/data/pg_hba.conf

# start db
su -l postgres -c "pg_ctl -D /var/lib/postgresql/data -l /tmp/logfile start"

su -l postgres -c "createdb db1"
su -l postgres -c "createdb db2"
su -l postgres -c "createdb db3"


DB_USER="postgres"
DB_NAMES=("db1" "db2" "db3")

for DB_NAME in "${DB_NAMES[@]}"; do
  # Check if the database exists
  if ! psql -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    # Database does not exist, create it
    echo "Creating database: $DB_NAME"
    createdb -U "$DB_USER" "$DB_NAME"
  else
    echo "Database '$DB_NAME' already exists"
  fi
done

