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

for DB in "${DATABASES[@]}"; do
  echo -e "${GREEN}Creating database:${NC} $DB"
  response=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "$COUCHDB_URL/$DB" -u "$COUCHDB_USERNAME:$COUCHDB_PASSWORD")

  if [ "$response" == "201" ]; then
    echo -e "${GREEN}Success:${NC} Database $DB created successfully."
  elif [ "$response" == "412" ]; then
    echo -e "${YELLOW}Notice:${NC} Database $DB already exists."
  else
    echo -e "${RED}Error:${NC} Failed to create database $DB. HTTP response code: $response."
    continue
  fi

  REPLICA_NAME="${DB}_replica"
  echo -e "${GREEN}Setting up replication for:${NC} $DB"
  replication_payload="{
    \"source\": {
      \"url\": \"$COUCHDB_URL/$DB\",
      \"headers\": {
        \"Authorization\": \"Basic $(echo -n "$COUCHDB_USERNAME:$COUCHDB_PASSWORD" | base64)\"
      }
    },
    \"target\": {
      \"url\": \"$COUCHDB_URL/$REPLICA_NAME\",
      \"headers\": {
        \"Authorization\": \"Basic $(echo -n "$COUCHDB_USERNAME:$COUCHDB_PASSWORD" | base64)\"
      }
    },
    \"create_target\": true,
    \"continuous\": true,
    \"owner\": \"$COUCHDB_USERNAME\"
  }"

  replication_response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$COUCHDB_URL/_replicator" \
    -u "$COUCHDB_USERNAME:$COUCHDB_PASSWORD" \
    -H "Content-Type: application/json" \
    -d "$replication_payload")

  if [ "$replication_response" == "201" ]; then
    echo -e "${GREEN}Success:${NC} Replication for $DB to $REPLICA_NAME created successfully."
  elif [ "$replication_response" == "409" ]; then
    echo -e "${YELLOW}Notice:${NC} Replication for $DB already exists."
  else
    echo -e "${RED}Error:${NC} Failed to set up replication for $DB. HTTP response code: $replication_response."
  fi
done

# Add a default admin user
echo -e "${GREEN}Creating default admin user:${NC} admin"
python3 add_default_admin.py

exit 0
