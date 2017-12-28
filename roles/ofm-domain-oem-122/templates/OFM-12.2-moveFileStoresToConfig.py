TRANSHOME='{{ ofmTransHome }}'
print 'Moving persistence stores to '+TRANSHOME
cd('/')
filestores = cmo.getFileStores();
for filestore in filestores:
    if not filestore.getDirectory().startswith(TRANSHOME):      
      print 'Moving persistence store'+filestore.getDirectory()+' to '+TRANSHOME
      filestore.setDirectory(TRANSHOME+'/'+filestore.getDirectory());

