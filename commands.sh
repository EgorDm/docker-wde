#!/bin/sh

ROOT=$(dirname $(realpath "$0"))
STORAGE="$ROOT/storage"
DC='sudo docker-compose'
D='sudo docker'

# TODO: this is temporary. Planning to move whole thing to python

wde_up() {
  pushd $ROOT
  if [ "$1" = "build" ]; then
    eval $DC up -d --build
  else
    eval $DC up -d
  fi
  popd
}

wde_restart() {
  pushd $ROOT
  eval $DC down && eval $DC up -d --build
  popd
}

wde_down() {
  pushd $ROOT
  eval $DC down
  popd
}

wde_exec() {
  echo "Running: $@"
  sudo docker exec -it wde bash -c "$@"
}

wde_unsecure() {
  DOMAIN=$1.dev
  DOMAIN_FOLDER=$1
  wde_exec "cd \$DOMAINS/$DOMAIN_FOLDER && valet unsecure"
  certutil -d sql:$HOME/.pki/nssdb -D -n "$DOMAIN" > /dev/null
  certutil -d $HOME/.mozilla/firefox/*.default -D -n "$DOMAIN" > /dev/null
}

wde_secure() {
  DOMAIN=$1.dev
  DOMAIN_FOLDER=$1
  certutil -d sql:$HOME/.pki/nssdb -D -n "$DOMAIN" > /dev/null
  certutil -d $HOME/.mozilla/firefox/*.default -D -n "$DOMAIN" > /dev/null

  wde_exec "cd \$DOMAINS/$DOMAIN_FOLDER && valet secure"
  certutil -d sql:$HOME/.pki/nssdb -A -t TC -n "$DOMAIN" -i "$STORAGE/valet/certificates/$DOMAIN.crt"
  certutil -d $HOME/.mozilla/firefox/*.default -A -t TC -n "$DOMAIN" -i "$STORAGE/valet/certificates/$DOMAIN.crt"
}

_wde_get_env() {
  RES="$(grep $1 $ROOT/.env | sed "s/$1.*=//")"
  if grep -q $1 $ROOT/.env; then 
    echo "$RES"
  else
  fi  
}

_wde_path_relative() {
  DOMAIN_PATH="$(_wde_get_env DOMAIN_PATH)"
  LOCAL_PATH="$(realpath $1)"
  LOCAL_PATH="$(realpath $LOCAL_PATH --relative-to=$DOMAIN_PATH)"
  if echo $LOCAL_PATH | grep -q '\.\./'; then
  else 
    echo "$LOCAL_PATH"
  fi
}

wde_db_import() {
  LOCAL_PATH="$(_wde_path_relative $1)"
  if [ -z $LOCAL_PATH ]; then
    echo "Given path must be relative to the domain path"
  else 
    DB_USER="$(_wde_get_env DB_USER)"
    DB_PASSWORD="$(_wde_get_env DB_PASSWORD)"

    wde_exec "mysql  -h 172.18.18.100 -uroot  -e \"GRANT ALL PRIVILEGES ON * . * TO '$DB_USER'@'%'\""    
    COMMAND="mysql -h 172.18.18.100 -u$DB_USER -p$DB_PASSWORD < \$DOMAINS/$LOCAL_PATH"
    wde_exec "$COMMAND"
  fi
  
}
