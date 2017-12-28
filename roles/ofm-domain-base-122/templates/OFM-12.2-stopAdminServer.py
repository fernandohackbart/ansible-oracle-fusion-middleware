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
  nmKill(ADMINSERVERNAME)
except Exception:
  print 'Admin Server '+ADMINSERVERNAME+' is already stopped, continuing...'
nmDisconnect()
exit()

