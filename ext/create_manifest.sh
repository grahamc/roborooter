#!/bin/bash

set -e

SRC="$1"
ORIG_ROOT=`pwd`

function _go_src {
  cd "$SRC"
}

function _go_orig {
  cd "$ORIG_ROOT"
}

# Host Detection
function is_darwin {
  uname -a | grep -i Darwin -q
}

function is_linux {
  uname -a | grep -i 'GNU/Linux' -q
}

# Host-Independant Implementations
function l_stat {
  if is_darwin; then
    stat -f '%Su:%Sg %Op %N' "$1" | awk '{ $2 = substr($2, 3); print }'
  elif is_linux; then
    stat -c "%U:%G 0%a %n" "$1"
  else
    echo "Cannot stat on unknown host." >&2
    exit 1
  fi
}

function l_readlink {
  if is_darwin; then
    readlink "$1"
  elif is_linux; then
    readlink -f "$1"
  else
    echo "Cannot readlink on unknown host." >&2
    exit 1
  fi
}

function create_md5 {
  _go_src
  find . -type f -print0 | xargs -0 md5sum
  _go_orig
}

function create_permissions {
  _go_src
  for f in `find . `; do
    l_stat "$f"
  done
  _go_orig
}

function create_devices {
  _go_src
  find . -type b -or -type c | awk '{ $2 = $1; $1 = substr($1, 2); print }'
  _go_orig
}

function create_whitelist {
  _go_src
  find . ! -type d
  find . -type f -name ".hint" | awk '{print substr($1, 1, length($1) - length(".hint"));}'
  _go_orig
}

function create_symlinks {
  _go_src
  for f in `find . -type l`; do
    src=`l_readlink "$f"`
    echo "$src $f"
  done
  _go_orig
}

mkdir -p "$2/manifests"

create_devices "$1" > "$2/manifests/devices"
create_md5 "$1" > "$2/manifests/md5"
create_permissions "$1" > "$2/manifests/permissions"
create_symlinks "$1" > "$2/manifests/symlinks"
create_whitelist "$1" > "$2/manifests/whitelist"

echo "Done, written to $2/manifests"

