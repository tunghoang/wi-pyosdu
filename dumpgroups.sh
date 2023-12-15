#!/bin/bash
XGROUPS=`python -m wi_pyosdu.entitlement --list_groups | jq -r ".groups[].email"`
XUSER=app@pvn.vn
for g in $XGROUPS; do
  echo "----$g-----"
  python -m wi_pyosdu.entitlement --list_members --group $g | jq -r ".members[].email"
done
