ADMINSERVERNAME='{{ ofmAdminserverName }}'
DOMAINNAME='{{ ofmDomainName }}'

print 'Changing the target AdminServer for  persistence stores to '+ADMINSERVERNAME
cd('/')
filestores = cmo.getFileStores();
for filestore in filestores:
  targets = filestore.getTargets()
  for target in targets:
    if target.getName()=='AdminServer':
      target.setName(ADMINSERVERNAME)
dumpStack()
