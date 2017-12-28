import os, sys
ADMINSERVERMACHINE='{{ ofmAdminserverMachine }}'
ADMINSERVERNAME='{{ ofmAdminserverName }}'
ADMINSERVERPORT='{{ ofmAdminserverPort }}'
ADMINPASSWORD='{{ ofmAdminPassword }}'
DOMAINNAME='{{ ofmDomainName }}'
USERHOMEDIR='{{ ofmInstallUserHomeDir }}'

ADMINSERVER_UP="false"

hideDumpStack("true")

while ADMINSERVER_UP!="true":
  print 'Waiting for '+ADMINSERVERNAME+' be up at: t3://'+ADMINSERVERMACHINE+':'+ADMINSERVERPORT
  try:
    java.lang.Thread.sleep(10000)
    connect('weblogic', ADMINPASSWORD, 't3://'+ADMINSERVERMACHINE+':'+ADMINSERVERPORT)
    storeUserConfig(USERHOMEDIR+'/bin/'+DOMAINNAME+'-cred.secure',USERHOMEDIR+'/bin/'+DOMAINNAME+'-key.secure')
    disconnect()
    ADMINSERVER_UP="true"
  except Exception:
    print 'Admin Server '+ADMINSERVERNAME+' not available at: t3://'+ADMINSERVERMACHINE+':'+ADMINSERVERPORT+' sleeping for 10s.'
    
