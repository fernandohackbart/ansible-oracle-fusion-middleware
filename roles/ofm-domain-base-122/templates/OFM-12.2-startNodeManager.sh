#!/bin/bash
umask 077
nohup {{ ofmDomainHome }}/bin/startNodeManager.sh >startNodeManager-{{ ofmDomainName }}.out 2>&1 &
