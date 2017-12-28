import os, sys
USERHOMEDIR='{{ ofmInstallUserHomeDir }}'
DOMAINSTAGEDIR='{{ ofmDomainStageDir }}'
ADMINSERVERMACHINE='{{ ofmAdminserverMachine }}'
ADMINSERVERNAME='{{ ofmAdminserverName }}'
ADMINSERVERPORT='{{ ofmAdminserverPort }}'
ADMINSERVERMSARGS='{{ ofmAdminservermsArsg }}'
DOMAINLOGDIR='{{ ofmDomainLogsHome }}'
DOMAINNAME='{{ ofmDomainName }}'
RESTRICTEDJRF='{{ ofmRestrictedJRF }}'

print 'Connecting to the '+ADMINSERVERNAME
connect(userConfigFile=USERHOMEDIR+'/bin/'+DOMAINNAME+'-cred.secure',userKeyFile=USERHOMEDIR+'/bin/'+DOMAINNAME+'-key.secure',url='t3://'+ADMINSERVERMACHINE+':'+ADMINSERVERPORT) 
edit()
startEdit()


if RESTRICTEDJRF.lower()=='false':
  execfile(DOMAINSTAGEDIR+'/OFM-12.2-configurePersistenceStores.py')

print 'Changing domain log location to '
cd('/Log/'+DOMAINNAME)
cmo.setFileName(DOMAINLOGDIR+'/'+DOMAINNAME+'.log')

execfile(DOMAINSTAGEDIR+'/OFM-12.2-adjustManagedServer-'+ADMINSERVERNAME+'.py')

print 'Done, activating and shutting down'
activate()
shutdown()
exit()

