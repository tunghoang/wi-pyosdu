#!/bin/bash
XGROUPS=`cat group.add`
for g in $XGROUPS; do
  echo $g
  python -m wi_pyosdu.entitlement --add2group --group $g --user wi@osdu.i2g.cloud 
  read
done
