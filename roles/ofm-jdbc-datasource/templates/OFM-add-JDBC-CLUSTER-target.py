USERHOMEDIR='{{ ofmInstallUserHomeDir }}'
ADMINSERVERMACHINE='{{ ofmAdminserverMachine }}'
ADMINSERVERNAME='{{ ofmAdminserverName }}'
ADMINSERVERPORT='{{ ofmAdminserverPort }}'
DOMAINNAME='{{ ofmDomainName }}'
DOMAINHOME='{{ ofmDomainHome }}'

JDBCDATASOURCENAME='{{ ofmJDBCDATASOURCENAME }}'
JDBCCLUSTERTARGET='{{ item }}'

print 'Connecting to the '+ADMINSERVERNAME
connect(userConfigFile=USERHOMEDIR+'/bin/'+DOMAINNAME+'-cred.secure',userKeyFile=USERHOMEDIR+'/bin/'+DOMAINNAME+'-key.secure',url='t3://'+ADMINSERVERMACHINE+':'+ADMINSERVERPORT) 
edit()
startEdit()
try:
  print 'Targeting JDBC datasource '+JDBCDATASOURCENAME+' to cluster '+JDBCCLUSTERTARGET
  cd('/JDBCSystemResources/'+JDBCDATASOURCENAME)
  cmo.addTarget(getMBean('/Clusters/'+JDBCCLUSTERTARGET))
  save()
  activate()
except Exception, e:
  print e
  print 'Datasource configuration error! Undoing the changes!'
  undo(defaultAnswer='y', unactivatedChanges='true')
  stopEdit('y')
exit()