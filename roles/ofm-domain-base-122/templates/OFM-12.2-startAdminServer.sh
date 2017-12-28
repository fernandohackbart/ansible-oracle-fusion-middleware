#!/bin/bash
nohup {{ ofmDomainHome }}/startWebLogic.sh >startWebLogic-{{ ofmAdminserverName }}.out 2>&1 &
