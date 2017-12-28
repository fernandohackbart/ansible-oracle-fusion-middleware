USERHOMEDIR='{{ ofmInstallUserHomeDir }}'
ADMINSERVERMACHINE='{{ ofmAdminserverMachine }}'
ADMINSERVERNAME='{{ ofmAdminserverName }}'
ADMINSERVERPORT='{{ ofmAdminserverPort }}'
DOMAINNAME='{{ ofmDomainName }}'
DOMAINHOME='{{ ofmDomainHome }}'

JDBCDATASOURCENAME='{{ ofmJDBCDATASOURCENAME }}'
JDBCMSTARGET='{{ item }}'

print 'Connecting to the '+ADMINSERVERNAME
connect(userConfigFile=USERHOMEDIR+'/bin/'+DOMAINNAME+'-cred.secure',userKeyFile=USERHOMEDIR+'/bin/'+DOMAINNAME+'-key.secure',url='t3://'+ADMINSERVERMACHINE+':'+ADMINSERVERPORT) 
edit()
startEdit()
try:
  print 'Targeting JDBC datasource '+JDBCDATASOURCENAME+' to managed server '+JDBCMSTARGET
  cd('/JDBCSystemResources/'+JDBCDATASOURCENAME)
  cmo.addTarget(getMBean('/Servers/'+JDBCMSTARGET))
  save()
  activate()
except Exception, e:
  print e
  print 'Datasource configuration error! Undoing the changes!'
  undo(defaultAnswer='y', unactivatedChanges='true')
  stopEdit('y')
exit()