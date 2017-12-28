import os, sys
ADMINSERVERMACHINE='{{ ofmAdminserverMachine }}'
ADMINSERVERNAME='{{ ofmAdminserverName }}'
DOMAINNAME='{{ ofmDomainName }}'
DOMAINHOME='{{ ofmDomainHome }}'
NODEMGRPORT='{{ ofmNodemgrPort }}'
NODEMGRUSERNAME='{{ ofmNodemgrUsername }}'
NODEMGRPASSWORD='{{ ofmNodemgrPassword }}'
nmConnect(NODEMGRUSERNAME,NODEMGRPASSWORD,ADMINSERVERMACHINE,NODEMGRPORT,DOMAINNAME,DOMAINHOME,'SSL')
try:
  nmStart(ADMINSERVERNAME)
except Exception:
  print 'Admin Server '+ADMINSERVERNAME+' is already running, continuing...'
nmDisconnect()
exit()

