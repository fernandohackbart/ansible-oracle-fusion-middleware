USERHOMEDIR='{{ ofmInstallUserHomeDir }}'
ADMINSERVERMACHINE='{{ ofmAdminserverMachine }}'
ADMINSERVERNAME='{{ ofmAdminserverName }}'
ADMINSERVERPORT='{{ ofmAdminserverPort }}'
DOMAINNAME='{{ ofmDomainName }}'
DOMAINHOME='{{ ofmDomainHome }}'

JDBCDATASOURCENAME='{{ ofmJDBCDATASOURCENAME }}'
JDBCURL='{{ ofmJDBCURL }}'
JDBCDRIVER='{{ ofmJDBCDriver }}'
JDBCJNDINAME='{{ ofmJDBCJNDI }}'
JDBCSCHEMA='{{ ofmJDBCSchema }}'
JDBCPASSWORD='{{ ofmJDBCPassword }}'
JDBCGLOBALTRANSACTIONSPROTOCOL='{{ ofmJDBCGlobalTransactionsProtocol }}'

print 'Connecting to the '+ADMINSERVERNAME
connect(userConfigFile=USERHOMEDIR+'/bin/'+DOMAINNAME+'-cred.secure',userKeyFile=USERHOMEDIR+'/bin/'+DOMAINNAME+'-key.secure',url='t3://'+ADMINSERVERMACHINE+':'+ADMINSERVERPORT) 
edit()
startEdit()
try:
  print 'Configuring JDBC datasource '+JDBCDATASOURCENAME+' pointing to jdbc:oracle:thin:@//'+JDBCURL
  cd('/')
  cmo.createJDBCSystemResource(JDBCDATASOURCENAME)
  cd('/JDBCSystemResources/'+JDBCDATASOURCENAME+'/JDBCResource/'+JDBCDATASOURCENAME)
  cmo.setName(JDBCDATASOURCENAME)
  print 'Set JNDI resources to '+JDBCJNDINAME
  cd('/JDBCSystemResources/'+JDBCDATASOURCENAME+'/JDBCResource/'+JDBCDATASOURCENAME+'/JDBCDataSourceParams/'+JDBCDATASOURCENAME)
  set('JNDINames',jarray.array([String(JDBCJNDINAME)], String))
  print 'Set URL to '+JDBCURL+' and driver to '+JDBCDRIVER
  cd('/JDBCSystemResources/'+JDBCDATASOURCENAME+'/JDBCResource/'+JDBCDATASOURCENAME+'/JDBCDriverParams/'+JDBCDATASOURCENAME)
  cmo.setUrl('jdbc:oracle:thin:@//'+JDBCURL)
  cmo.setDriverName(JDBCDRIVER)
  set('PasswordEncrypted', encrypt(JDBCPASSWORD,DOMAINHOME))
  print 'Set test table name'
  cd('/JDBCSystemResources/'+JDBCDATASOURCENAME+'/JDBCResource/'+JDBCDATASOURCENAME+'/JDBCConnectionPoolParams/'+JDBCDATASOURCENAME)
  cmo.setTestTableName('SQL ISVALID\r\n\r\n')
  print 'Create user property'
  cd('/JDBCSystemResources/'+JDBCDATASOURCENAME+'/JDBCResource/'+JDBCDATASOURCENAME+'/JDBCDriverParams/'+JDBCDATASOURCENAME+'/Properties/'+JDBCDATASOURCENAME)
  cmo.createProperty('user')
  print 'Set user property'
  cd('/JDBCSystemResources/'+JDBCDATASOURCENAME+'/JDBCResource/'+JDBCDATASOURCENAME+'/JDBCDriverParams/'+JDBCDATASOURCENAME+'/Properties/'+JDBCDATASOURCENAME+'/Properties/user')
  cmo.setValue(JDBCSCHEMA)
  print 'Set user setGlobalTransactionsProtocol='+JDBCGLOBALTRANSACTIONSPROTOCOL
  cd('/JDBCSystemResources/'+JDBCDATASOURCENAME+'/JDBCResource/'+JDBCDATASOURCENAME+'/JDBCDataSourceParams/'+JDBCDATASOURCENAME)
  cmo.setGlobalTransactionsProtocol(JDBCGLOBALTRANSACTIONSPROTOCOL)
  save()
  activate()
except Exception, e:
  print e
  print 'Datasource configuration error! Undoing the changes!'
  undo(defaultAnswer='y', unactivatedChanges='true')
  stopEdit('y')
exit()