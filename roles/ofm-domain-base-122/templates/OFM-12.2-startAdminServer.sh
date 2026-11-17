#!/bin/bash
umask 077
nohup {{ ofmDomainHome }}/startWebLogic.sh >startWebLogic-{{ ofmAdminserverName }}.out 2>&1 &
