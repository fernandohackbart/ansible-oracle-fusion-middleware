import os, sys
USERHOMEDIR='{{ ofmInstallUserHomeDir }}'
RESTRICTEDJRF='{{ ofmRestrictedJRF }}'
EXTCLUSTERNAME='{{ ofmFRMextclustername }}'
EXTSERVERPREFIX='{{ ofmFRMextserverprefix }}'
EXTSERVERGROUPS='{{ ofmFRMextservergroups }}'
EXTPROVIDESERVER='{{ ofmFRMextprovideserver }}'
EXTPROVIDEDSERVERNAME='{{ ofmFRMextprovidedservername }}'
EXTSERVERNAME='{{ ofmFRMextservername }}'
EXTASSIGNEXISTINGSERVER='{{ ofmFRMextprovideserver }}'
ADMINSERVERMACHINE='{{ ofmAdminserverMachine }}'
ADMINSERVERNAME='{{ ofmAdminserverName }}'
ADMINSERVERPORT='{{ ofmAdminserverPort }}'
DOMAINNAME='{{ ofmDomainName }}'
ADJUSTSERVERNAME='{{ ofmFRMextserverprefix }}{{ item.0}}'
ADJUSTSERVERMSARGS='{{ ofmFRMextmsargs }}'
ADJUSTSERVERMACHINE='{{ item.1 }}'
ADJUSTSERVERPORT='{{ ofmFRMextmsport }}'
ADJUSTSERVERLOGDIR='{{ ofmDomainLogsHome }}/{{ ofmFRMextserverprefix }}{{ item.0}}'
NODEMGRPORT='{{ ofmNodemgrPort }}'
JDBCRCUSCHEMAPREFIX='{{ ofmJdbcRCUSchemaPrefix }}'


if ADMINSERVERNAME!=ADJUSTSERVERNAME:
  connect(userConfigFile=USERHOMEDIR+'/bin/'+DOMAINNAME+'-cred.secure',userKeyFile=USERHOMEDIR+'/bin/'+DOMAINNAME+'-key.secure',url='t3://'+ADMINSERVERMACHINE+':'+ADMINSERVERPORT) 
  edit()
  startEdit()

cd('/Servers/'+ADJUSTSERVERNAME)
 
cd('/Servers/'+ADJUSTSERVERNAME+'/Log/'+ADJUSTSERVERNAME)
cmo.setFileName(ADJUSTSERVERLOGDIR+'/'+ADJUSTSERVERNAME+'.log')
cd('/Servers/'+ADJUSTSERVERNAME+'/WebServer/'+ADJUSTSERVERNAME+'/WebServerLog/'+ADJUSTSERVERNAME)
cmo.setFileName(ADJUSTSERVERLOGDIR+'/access.log')
cd('/Servers/'+ADJUSTSERVERNAME+'/DataSource/'+ADJUSTSERVERNAME+'/DataSourceLogFile/'+ADJUSTSERVERNAME)
cmo.setFileName(ADJUSTSERVERLOGDIR+'/datasource.log')
cd('/Servers/'+ADJUSTSERVERNAME+'/ServerDiagnosticConfig/'+ADJUSTSERVERNAME)
cmo.setImageDir(ADJUSTSERVERLOGDIR+'/diagnostic_images')

cd('/Servers/'+ADJUSTSERVERNAME+'/ServerStart/'+ADJUSTSERVERNAME)
NEW_ARGUMENTS=' -Djava.security.egd=file:/dev/./urandom -Dweblogic.Stdout='+ADJUSTSERVERLOGDIR+'/'+ADJUSTSERVERNAME+'.out -Dweblogic.Stderr='+ADJUSTSERVERLOGDIR+'/'+ADJUSTSERVERNAME+'.out -Djava.net.preferIPv4Stack=true -Dsvnkit.useJNA=false -Djava.awt.headless=true '
if (ADJUSTSERVERMSARGS!=None):
  NEW_ARGUMENTS=ADJUSTSERVERMSARGS+NEW_ARGUMENTS
ARGUMENTS = cmo.getArguments()

if ARGUMENTS != None:
  cmo.setArguments(ARGUMENTS+NEW_ARGUMENTS)
else:
  cmo.setArguments(NEW_ARGUMENTS)


#http://docs.oracle.com/cd/E24329_01/web.1211/e24422/ssl.htm#SECMG573
#http://docs.oracle.com/cd/E24329_01/apirefs.1211/e24401/taskhelp/security/ConfigureACustomHostNameVerifier.html#WLACH03008
cd('/Servers/'+ADJUSTSERVERNAME+'/SSL/'+ADJUSTSERVERNAME)
cmo.setHostnameVerifier('weblogic.security.utils.SSLWLSWildcardHostnameVerifier')
cmo.setHostnameVerificationIgnored(false)
cmo.setTwoWaySSLEnabled(false)
cmo.setClientCertificateEnforced(false)


#http://docs.oracle.com/middleware/1213/core/ASADM/logs.htm#ASADM229
logsNotChange=['console-handler','wls-domain','quicktrace-handler']
lh = listLogHandlers(target=ADJUSTSERVERNAME)
for l in lh:
  lname = l.get('name')
  if lname not in logsNotChange:
    lprops = l.get('properties')
    for prop in lprops:
      if prop.get('name') == 'path':
        pathOld = prop.get('value')
    pathNew1 = pathOld.replace('${domain.home}/servers/${weblogic.Name}',ADJUSTSERVERLOGDIR)
    pathNew = pathNew1.replace('${weblogic.Name}/logs','${weblogic.Name}')
    configureLogHandler(target=ADJUSTSERVERNAME,name=lname,path=pathNew)

cd('/Servers/'+ADJUSTSERVERNAME)
cmo.setListenPort(int(ADJUSTSERVERPORT))

cd('/Servers/'+ADJUSTSERVERNAME)
if (getMBean('/Machines/'+ADJUSTSERVERMACHINE)==None):
  cd('/')
  create(ADJUSTSERVERMACHINE, 'Machine')
  cd('/Machines/'+ADJUSTSERVERMACHINE+'/NodeManager/'+ADJUSTSERVERMACHINE)
  set('ListenAddress',ADJUSTSERVERMACHINE)
  cmo.setListenPort(int(NODEMGRPORT))
  set('NMType', 'SSL')
  cd('/')

  #Add the machine to the coherence cluster
  #export COHERENCE_CLUSTER_NAME=defaultCoherenceCluster
  #export COHERENCE_UNICAST_PORT=9995
  #export COHERENCE_CLUSTER_WKA0=${MACHINENAME}
  #COHERENCE_CLUSTER_WKA_CREATE=COHERENCE_CLUSTER_WKA0
  #cd('/CoherenceClusterSystemResources/'+COHERENCE_CLUSTER_NAME+'/CoherenceClusterResource/'+COHERENCE_CLUSTER_NAME+'/CoherenceClusterParams/'+COHERENCE_CLUSTER_NAME+'/CoherenceClusterWellKnownAddresses/'+COHERENCE_CLUSTER_NAME)
  #cmo.createCoherenceClusterWellKnownAddress(COHERENCE_CLUSTER_WKA_CREATE)
  #cd('/CoherenceClusterSystemResources/'+COHERENCE_CLUSTER_NAME+'/CoherenceClusterResource/'+COHERENCE_CLUSTER_NAME+'/CoherenceClusterParams/'+COHERENCE_CLUSTER_NAME+'/CoherenceClusterWellKnownAddresses/'+COHERENCE_CLUSTER_NAME+'/CoherenceClusterWellKnownAddresses/'+COHERENCE_CLUSTER_WKA_CREATE)
  #cmo.setListenPort(int(COHERENCE_UNICAST_PORT))
  #cmo.setListenAddress(COHERENCE_CLUSTER_WKA_CREATE)

cd('/Servers/'+ADJUSTSERVERNAME)
cmo.setMachine(getMBean('/Machines/'+ADJUSTSERVERMACHINE))

if RESTRICTEDJRF.lower()=='false':
  cd('/JDBCSystemResources/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS')
  cmo.addTarget(getMBean('/Servers/'+ADJUSTSERVERNAME))
  cd('/Servers/'+ADJUSTSERVERNAME+'/TransactionLogJDBCStore/'+ADJUSTSERVERNAME)
  cmo.setDataSource(getMBean('/JDBCSystemResources/'+JDBCRCUSCHEMAPREFIX+'_WLS-DS'))
  cmo.setPrefixName('TLOG_'+ADJUSTSERVERNAME)
  cmo.setEnabled(true)

if ADMINSERVERNAME!=ADJUSTSERVERNAME:
  activate()
  exit()