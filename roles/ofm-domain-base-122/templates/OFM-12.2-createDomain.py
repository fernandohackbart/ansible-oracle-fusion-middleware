import os, sys
VERSION='{{ ofmVersion }}'
DOMAINSTAGEDIR='{{ ofmDomainStageDir }}'
DOMAINHOME='{{ ofmDomainHome }}'
ADMINSERVERMACHINE='{{ ofmAdminserverMachine }}'
ADMINSERVERNAME='{{ ofmAdminserverName }}'
ADMINSERVERPORT='{{ ofmAdminserverPort }}'
TEMPLATEDOMAINNAME='{{ ofmTemplateDomainName }}'
ADMINPASSWORD='{{ ofmAdminPassword }}'
APPLICATIONHOME='{{ ofmApplicationHome }}'
NODEMGRPORT='{{ ofmNodemgrPort }}'
NODEMGRUSERNAME='{{ ofmNodemgrUsername }}'
NODEMGRPASSWORD='{{ ofmNodemgrPassword }}'
JDBCURLRCU='{{ ofmJdbcURLrcu }}'
JDBCRCUPASSWORD='{{ ofmJdbcRCUPassword }}'
TEMPLATEJDBCPREFIX='{{ ofmTemplateJDBCPrefix }}'
JDBCRCUSCHEMAPREFIX='{{ ofmJdbcRCUSchemaPrefix }}'
RESTRICTEDJRF='{{ ofmRestrictedJRF }}'

print 'Reading base template..'
selectTemplate('Basic WebLogic Server Domain',VERSION)
loadTemplates()

execfile(DOMAINSTAGEDIR+'/OFM-12.2-moveFileStoresToConfig.py')

print 'Changing AdminServ attributes'
cd('/Servers/AdminServer')
set('Name',ADMINSERVERNAME)
set('ListenAddress','')
set('ListenPort',int(ADMINSERVERPORT))

print 'Changing basic configuration'
cd('/Security/'+TEMPLATEDOMAINNAME+'/User/weblogic')
cmo.setPassword(ADMINPASSWORD)

setOption('AppDir',APPLICATIONHOME)
setOption('ServerStartMode','prod')
setOption('OverwriteDomain', 'true')

print 'Changing nodemanager properties'
cd('/NMProperties')
set('ListenAddress',ADMINSERVERMACHINE)
set('ListenPort',NODEMGRPORT)
print 'Changing nodemanager password'
cd('/SecurityConfiguration/'+TEMPLATEDOMAINNAME)
cmo.setNodeManagerUsername(NODEMGRUSERNAME)
cmo.setNodeManagerPasswordEncrypted(NODEMGRPASSWORD)

print 'Writing the domain'
writeDomain(DOMAINHOME)
closeTemplate()

if RESTRICTEDJRF.lower()=='false':
  readDomain(DOMAINHOME)
  selectTemplate('Oracle JRF',VERSION)
  loadTemplates()
  cd('/JDBCSystemResource/LocalSvcTblDataSource/JdbcResource/LocalSvcTblDataSource/JDBCDriverParams/NO_NAME_0')
  set('DriverName','oracle.jdbc.OracleDriver')
  set('URL','jdbc:oracle:thin:@//'+JDBCURLRCU)
  set('PasswordEncrypted',JDBCRCUPASSWORD)
  cd('/JDBCSystemResource/LocalSvcTblDataSource/JdbcResource/LocalSvcTblDataSource/JDBCDriverParams/NO_NAME_0/Properties/NO_NAME_0/Property/user')
  print 'Configuring user '+cmo.getValue().replace(TEMPLATEJDBCPREFIX,JDBCRCUSCHEMAPREFIX)
  cmo.setValue(cmo.getValue().replace(TEMPLATEJDBCPREFIX,JDBCRCUSCHEMAPREFIX))
  getDatabaseDefaults()
  updateDomain()
  closeDomain()
else:
  readDomain(DOMAINHOME)
  selectTemplate('Oracle Restricted JRF',VERSION)
  loadTemplates()
  updateDomain()
  closeDomain()
exit()
