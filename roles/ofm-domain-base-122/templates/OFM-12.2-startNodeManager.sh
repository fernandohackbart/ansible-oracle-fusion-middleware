#!/bin/bash
nohup {{ ofmDomainHome }}/bin/startNodeManager.sh >startNodeManager-{{ ofmDomainName }}.out 2>&1 &
