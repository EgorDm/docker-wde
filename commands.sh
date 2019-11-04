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
