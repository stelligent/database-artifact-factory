#!/bin/bash

if [ "$#" != 3 ]; then
  echo "Usage: $0 db_host db_name user"
  exit 1
fi
create_db_script='create_schema.sql'
database="$2"
hostname="$1"
port='5432'
user="$3"

createdb -h $hostname -U $user -p $port $database
psql -d $database -h $hostname -U $user -p $port -f $create_db_script
psql -d $database -h $hostname -U $user -p $port -c "\copy person (firstname,lastname,state) FROM 'sample_person_data.csv' delimiter ',' csv;"


