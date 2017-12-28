#TODO: check why it does not accept the TNS URL 
#JDBCURLRCU='{{ ofmJdbcURL }}'
JDBCURLRCU='{{ ofmJdbcURLrcu }}'
JDBCRCUSCHEMAPREFIX='{{ ofmJdbcRCUSchemaPrefix }}'
JDBCRCUPASSWORD='{{ ofmJdbcRCUPassword }}'
DOMAINHOME='{{ ofmDomainHome }}'

print 'Create a datasource to hold the database based stores'
cd('/')
cmo.createJDBCSystemResource(JDBCRCUSCHEMAPREFIX+'_WLS-DS')
cd('/JDBCSystemResources/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS/JDBCResource/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS')
cmo.setName(JDBCRCUSCHEMAPREFIX+'_WLS-DS')
cd('/JDBCSystemResources/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS/JDBCResource/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS/JDBCDataSourceParams/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS')
set('JNDINames',jarray.array([String('jdbc/'+JDBCRCUSCHEMAPREFIX+'_WLS')], String))
cd('/JDBCSystemResources/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS/JDBCResource/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS/JDBCDriverParams/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS')
cmo.setUrl('jdbc:oracle:thin:@//'+JDBCURLRCU)
cmo.setDriverName('oracle.jdbc.OracleDriver')
set('PasswordEncrypted', encrypt(JDBCRCUPASSWORD,DOMAINHOME))
cd('/JDBCSystemResources/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS/JDBCResource/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS/JDBCConnectionPoolParams/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS')
cmo.setTestTableName('SQL ISVALID\r\n\r\n')
cd('/JDBCSystemResources/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS/JDBCResource/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS/JDBCDriverParams/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS/Properties/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS')
cmo.createProperty('user')
cd('/JDBCSystemResources/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS/JDBCResource/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS/JDBCDriverParams/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS/Properties/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS/Properties/user')
cmo.setValue(JDBCRCUSCHEMAPREFIX+'_WLS')
cd('/JDBCSystemResources/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS/JDBCResource/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS/JDBCDataSourceParams/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS')
cmo.setGlobalTransactionsProtocol('None')



