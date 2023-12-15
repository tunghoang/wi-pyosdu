#!/bin/bash
XGROUPS=`cat group.add`
XUSER=app@pvn.vn
for g in $XGROUPS; do
  echo $g
  python -m wi_pyosdu.entitlement --add2group --group $g --user $XUSER
  read
done
