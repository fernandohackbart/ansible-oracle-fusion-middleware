import os, sys
EXTTEMPLATE='{{ ofmOEMexttemplate }}'
EXTVERSION='{{ ofmOEMextversion }}'
DOMAINSTAGEDIR='{{ ofmDomainStageDir }}'
DOMAINHOME='{{ ofmDomainHome }}'
RESTRICTEDJRF='{{ ofmRestrictedJRF }}'

print 'Reading the domain'
readDomain(DOMAINHOME)

print 'Loading template: '+EXTTEMPLATE
selectTemplate(EXTTEMPLATE,EXTVERSION)
loadTemplates()

execfile(DOMAINSTAGEDIR+'/OFM-12.2-moveFileStoresToConfig.py')

print 'Configuring the database connections'
if RESTRICTEDJRF.lower()=='false':
  getDatabaseDefaults()

print 'Updating '+DOMAINHOME+' domain...'
updateDomain()
closeDomain()


