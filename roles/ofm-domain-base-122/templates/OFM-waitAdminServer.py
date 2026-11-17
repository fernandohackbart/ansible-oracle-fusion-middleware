import os, sys
ADMINSERVERMACHINE='{{ ofmAdminserverMachine }}'
ADMINSERVERNAME='{{ ofmAdminserverName }}'
ADMINSERVERPORT='{{ ofmAdminserverPort }}'
ADMINPASSWORD='{{ ofmAdminPassword }}'
DOMAINNAME='{{ ofmDomainName }}'
USERHOMEDIR='{{ ofmInstallUserHomeDir }}'

MAX_ATTEMPTS=60
ATTEMPT=0
ADMINSERVER_UP="false"

hideDumpStack("true")

while ADMINSERVER_UP != "true" and ATTEMPT < MAX_ATTEMPTS:
  ATTEMPT = ATTEMPT + 1
  print 'Waiting for '+ADMINSERVERNAME+' at t3://'+ADMINSERVERMACHINE+':'+ADMINSERVERPORT+' (attempt '+str(ATTEMPT)+'/'+str(MAX_ATTEMPTS)+')'
  try:
    java.lang.Thread.sleep(10000)
    connect('weblogic', ADMINPASSWORD, 't3://'+ADMINSERVERMACHINE+':'+ADMINSERVERPORT)
    storeUserConfig(USERHOMEDIR+'/bin/'+DOMAINNAME+'-cred.secure',USERHOMEDIR+'/bin/'+DOMAINNAME+'-key.secure')
    disconnect()
    ADMINSERVER_UP="true"
  except Exception:
    print 'Admin Server '+ADMINSERVERNAME+' not available; sleeping for 10s.'

if ADMINSERVER_UP != "true":
  raise Exception('Admin Server '+ADMINSERVERNAME+' did not start after '+str(MAX_ATTEMPTS)+' attempts.')
