import os, sys
ADMINSERVERMACHINE='{{ ofmAdminserverMachine }}'
ADMINSERVERNAME='{{ ofmAdminserverName }}'
DOMAINNAME='{{ ofmDomainName }}'
DOMAINHOME='{{ ofmDomainHome }}'
NODEMGRPORT='{{ ofmNodemgrPort }}'
NODEMGRUSERNAME='{{ ofmNodemgrUsername }}'
NODEMGRPASSWORD='{{ ofmNodemgrPassword }}'
USERHOMEDIR='{{ ofmInstallUserHomeDir }}'

nmConnect(userConfigFile=USERHOMEDIR+'/bin/'+DOMAINNAME+'-nodemanager.config', userKeyFile=userKeyFile=USERHOMEDIR+'/bin/'+DOMAINNAME+'-nodemanager.keyfile',ADMINSERVERMACHINE,NODEMGRPORT,DOMAINNAME,DOMAINHOME,'SSL'); 
try:
  nmKill(ADMINSERVERNAME)
except Exception:
  print 'Admin Server '+ADMINSERVERNAME+' is already stopped, continuing...'
nmDisconnect()
exit()

