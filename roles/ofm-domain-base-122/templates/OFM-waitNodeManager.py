import os, sys
ADMINSERVERMACHINE='{{ ofmAdminserverMachine }}'
ADMINSERVERNAME='{{ ofmAdminserverName }}'
DOMAINNAME='{{ ofmDomainName }}'
DOMAINHOME='{{ ofmDomainHome }}'
NODEMGRPORT='{{ ofmNodemgrPort }}'
NODEMGRUSERNAME='{{ ofmNodemgrUsername }}'
NODEMGRPASSWORD='{{ ofmNodemgrPassword }}'
USERHOMEDIR='{{ ofmInstallUserHomeDir }}'

MAX_ATTEMPTS=60
ATTEMPT=0
NODEMANAGER_UP="false"

hideDumpStack("true")

while NODEMANAGER_UP != "true" and ATTEMPT < MAX_ATTEMPTS:
  ATTEMPT = ATTEMPT + 1
  print 'Waiting for NodeManager at '+ADMINSERVERMACHINE+':'+NODEMGRPORT+' (attempt '+str(ATTEMPT)+'/'+str(MAX_ATTEMPTS)+')'
  try:
    java.lang.Thread.sleep(10000)
    nmConnect(NODEMGRUSERNAME,NODEMGRPASSWORD,ADMINSERVERMACHINE,NODEMGRPORT,DOMAINNAME,DOMAINHOME,'SSL')
    storeUserConfig(USERHOMEDIR+'/bin/'+DOMAINNAME+'-nodemanager.config',USERHOMEDIR+'/bin/'+DOMAINNAME+'-nodemanager.keyfile','true')
    nmDisconnect()
    NODEMANAGER_UP="true"
  except Exception:
    print 'NodeManager not available; sleeping for 10s.'

if NODEMANAGER_UP != "true":
  raise Exception('NodeManager did not start after '+str(MAX_ATTEMPTS)+' attempts.')
