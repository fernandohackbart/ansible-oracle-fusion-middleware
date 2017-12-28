import os, sys
ADMINSERVERMACHINE='{{ ofmAdminserverMachine }}'
ADMINSERVERNAME='{{ ofmAdminserverName }}'
DOMAINNAME='{{ ofmDomainName }}'
DOMAINHOME='{{ ofmDomainHome }}'
NODEMGRPORT='{{ ofmNodemgrPort }}'
NODEMGRUSERNAME='{{ ofmNodemgrUsername }}'
NODEMGRPASSWORD='{{ ofmNodemgrPassword }}'
USERHOMEDIR='{{ ofmInstallUserHomeDir }}'

nmConnect(userConfigFile=USERHOMEDIR+'/bin/'+DOMAINNAME+'-nodemanager.config', userKeyFile=USERHOMEDIR+'/bin/'+DOMAINNAME+'-nodemanager.keyfile',host=ADMINSERVERMACHINE,port=NODEMGRPORT,domainName=DOMAINNAME,domainDir=DOMAINHOME,nmType='SSL');
try:
  nmStart(ADMINSERVERNAME)
except Exception:
  print 'Admin Server '+ADMINSERVERNAME+' is already running, continuing...'
nmDisconnect()
exit()
