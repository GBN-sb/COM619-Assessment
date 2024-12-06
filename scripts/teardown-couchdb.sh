#!/bin/bash

RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

missing_env_vars=0

if [ -z "$COUCHDB_URL" ]; then
  echo -e "${RED}Error:${NC} Environment variable ${YELLOW}COUCHDB_URL${NC} is not set."
  missing_env_vars=1
fi

if [ -z "$COUCHDB_USERNAME" ]; then
  echo -e "${RED}Error:${NC} Environment variable ${YELLOW}COUCHDB_USERNAME${NC} is not set."
  missing_env_vars=1
fi

if [ -z "$COUCHDB_PASSWORD" ]; then
  echo -e "${RED}Error:${NC} Environment variable ${YELLOW}COUCHDB_PASSWORD${NC} is not set."
  missing_env_vars=1
fi

if [ $missing_env_vars -eq 1 ]; then
  echo -e "${YELLOW}Hint:${NC} You can set these variables using the following commands:"
  echo -e "  export ${YELLOW}COUCHDB_URL${NC}=\"http://localhost:5984\""
  echo -e "  export ${YELLOW}COUCHDB_USERNAME${NC}=\"admin\""
  echo -e "  export ${YELLOW}COUCHDB_PASSWORD${NC}=\"password\""
  echo -e "${RED}Exiting.${NC}"
  exit 0
fi

DATABASES=("recipes" "users" "comments" "likes")
echo -e "${GREEN}Clearing all replication entries in the _replicator database...${NC}"
replication_ids=$(curl -s -u "$COUCHDB_USERNAME:$COUCHDB_PASSWORD" "$COUCHDB_URL/_replicator/_all_docs" \
    | jq -r ".rows[].id")

if [ -z "$replication_ids" ]; then
    echo -e "${YELLOW}Notice:${NC} No replication entries found in the _replicator database."
else
    for replication_id in $replication_ids; do
        rev=$(curl -s -u "$COUCHDB_USERNAME:$COUCHDB_PASSWORD" "$COUCHDB_URL/_replicator/$replication_id" \
                | jq -r "._rev")
        echo "Replication ID: $replication_id, Rev: $rev"
        delete_replication_response=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$COUCHDB_URL/_replicator/$replication_id?rev=$rev" \
            -u "$COUCHDB_USERNAME:$COUCHDB_PASSWORD")

        if [ "$delete_replication_response" == "200" ]; then
            echo -e "${GREEN}Success:${NC} Deleted replication entry with ID: $replication_id."
        else
            echo -e "${RED}Error:${NC} Failed to delete replication entry with ID: $replication_id. HTTP response code: $delete_replication_response."
        fi
    done
fi

for DB in "${DATABASES[@]}"; do
  REPLICA_NAME="${DB}_replica"

  echo -e "${GREEN}Deleting database:${NC} $DB"
  delete_db_response=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$COUCHDB_URL/$DB" \
    -u "$COUCHDB_USERNAME:$COUCHDB_PASSWORD")

  if [ "$delete_db_response" == "200" ]; then
    echo -e "${GREEN}Success:${NC} Database $DB deleted successfully."
  elif [ "$delete_db_response" == "404" ]; then
    echo -e "${YELLOW}Notice:${NC} Database $DB does not exist."
  else
    echo -e "${RED}Error:${NC} Failed to delete database $DB. HTTP response code: $delete_db_response."
  fi

  echo -e "${GREEN}Deleting replica database:${NC} $REPLICA_NAME"
  delete_replica_response=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$COUCHDB_URL/$REPLICA_NAME" \
    -u "$COUCHDB_USERNAME:$COUCHDB_PASSWORD")

  if [ "$delete_replica_response" == "200" ]; then
    echo -e "${GREEN}Success:${NC} Replica database $REPLICA_NAME deleted successfully."
  elif [ "$delete_replica_response" == "404" ]; then
    echo -e "${YELLOW}Notice:${NC} Replica database $REPLICA_NAME does not exist."
  else
    echo -e "${RED}Error:${NC} Failed to delete replica database $REPLICA_NAME. HTTP response code: $delete_replica_response."
  fi
done

exit 0
