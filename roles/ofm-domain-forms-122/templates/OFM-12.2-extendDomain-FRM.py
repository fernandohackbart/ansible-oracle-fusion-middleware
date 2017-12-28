import os, sys
EXTTEMPLATE='{{ ofmFRMexttemplate }}'
EXTVERSION='{{ ofmFRMextversion }}'
DOMAINSTAGEDIR='{{ ofmDomainStageDir }}'
DOMAINHOME='{{ ofmDomainHome }}'
RESTRICTEDJRF='{{ ofmRestrictedJRF }}'
EXTCLUSTERNAME='{{ ofmFRMextclustername }}'
EXTSERVERPREFIX='{{ ofmFRMextserverprefix }}'
EXTSERVERGROUPS='{{ ofmFRMextservergroups }}'
EXTPROVIDESERVER='{{ ofmFRMextprovideserver }}'
EXTPROVIDEDSERVERNAME='{{ ofmFRMextprovidedservername }}'
EXTSERVERNAME='{{ ofmFRMextservername }}'
EXTASSIGNEXISTINGSERVER='{{ ofmFRMextassignexistingserver }}'

print 'Reading the domain'
readDomain(DOMAINHOME)

print 'Loading template: '+EXTTEMPLATE
selectTemplate(EXTTEMPLATE,EXTVERSION)
loadTemplates()

execfile(DOMAINSTAGEDIR+'/OFM-12.2-moveFileStoresToConfig.py')

if EXTCLUSTERNAME!='':
  try:
    print 'Creating the cluster '+EXTCLUSTERNAME
    cd('/')
    create(EXTCLUSTERNAME, 'Cluster')
    cd('/Clusters/'+EXTCLUSTERNAME)
    cmo.setClusterMessagingMode('unicast')
  except Exception, e:
    print e
    print 'Cluster '+EXTCLUSTERNAME+' already exists! Ignoring'
	
if EXTPROVIDESERVER.lower()=='true':
  print 'Rename '+EXTPROVIDEDSERVERNAME+' to '+EXTSERVERNAME
  cd('/Servers/'+EXTPROVIDEDSERVERNAME) 
  cmo.setName(EXTSERVERNAME)
  assign('Server',EXTSERVERNAME,'Cluster',EXTCLUSTERNAME)
  if EXTSERVERGROUPS != '':
    setServerGroups(EXTSERVERNAME,EXTSERVERGROUPS.split(','))

if EXTASSIGNEXISTINGSERVER!='':	
  if EXTSERVERGROUPS !='':
    setServerGroups(EXTASSIGNEXISTINGSERVER,EXTSERVERGROUPS.split(','))

print 'Configuring the database connections'
if RESTRICTEDJRF.lower()=='false':
  getDatabaseDefaults()

print 'Updating '+DOMAINHOME+' domain...'
updateDomain()
closeDomain()


