import os, sys
ADMINSERVERMACHINE='{{ ofmAdminserverMachine }}'
ADMINSERVERNAME='{{ ofmAdminserverName }}'
DOMAINNAME='{{ ofmDomainName }}'
DOMAINHOME='{{ ofmDomainHome }}'
NODEMGRPORT='{{ ofmNodemgrPort }}'
NODEMGRUSERNAME='{{ ofmNodemgrUsername }}'
NODEMGRPASSWORD='{{ ofmNodemgrPassword }}'
USERHOMEDIR='{{ ofmInstallUserHomeDir }}'
NODEMANAGER_UP="false"

hideDumpStack("true")

while NODEMANAGER_UP!="true":
  print 'Waiting for NodeManager to listen '+ADMINSERVERMACHINE+':'+NODEMGRPORT
  try:
    java.lang.Thread.sleep(10000)
    nmConnect(NODEMGRUSERNAME,NODEMGRPASSWORD,ADMINSERVERMACHINE,NODEMGRPORT,DOMAINNAME,DOMAINHOME,'SSL')
    storeUserConfig(USERHOMEDIR+'/bin/'+DOMAINNAME+'-nodemanager.config',USERHOMEDIR+'/bin/'+DOMAINNAME+'-nodemanager.keyfile','true');
    nmDisconnect()
    NODEMANAGER_UP="true"
  except Exception:
    print 'NodeManager not available at: '+ADMINSERVERMACHINE+':'+NODEMGRPORT+' sleeping for 10s.'
    
