import os, sys
DOMAINHOME='{{ ofmDomainHome }}'
EXTCLUSTERNAME='{{ ofmFRMextclustername }}'
EXTSERVERPREFIX='{{ ofmFRMextserverprefix }}'
EXTSERVERGROUPS='{{ ofmFRMextservergroups }}'
EXTSERVERINDEX='{{ item.0 }}'

print 'Reading the domain'
readDomain(DOMAINHOME)

print 'Creating the managed server '+EXTSERVERPREFIX+EXTSERVERINDEX
cd('/')
create(EXTSERVERPREFIX+EXTSERVERINDEX, 'Server')

#Get the server groups from the config-groups.xml file inside the template .jar file

cd('/Servers/'+EXTSERVERPREFIX+EXTSERVERINDEX)
if EXTSERVERGROUPS!=None:
  setServerGroups(EXTSERVERPREFIX+EXTSERVERINDEX,EXTSERVERGROUPS.split(','))
assign('Server',EXTSERVERPREFIX+EXTSERVERINDEX,'Cluster',EXTCLUSTERNAME)
cd('/')

print 'Updating '+DOMAINHOME+' domain...'
updateDomain()
print 'Successfully Updated '+DOMAINHOME+' domain.'
closeDomain()
exit()
