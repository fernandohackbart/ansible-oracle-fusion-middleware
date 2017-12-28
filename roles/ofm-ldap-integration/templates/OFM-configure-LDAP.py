USERHOMEDIR='{{ ofmInstallUserHomeDir }}'
ADMINSERVERMACHINE='{{ ofmAdminserverMachine }}'
ADMINSERVERNAME='{{ ofmAdminserverName }}'
ADMINSERVERPORT='{{ ofmAdminserverPort }}'
DOMAINNAME='{{ ofmDomainName }}'
LDAPPROVIDERNAME='{{ ofmLDAPProviderName }}'
LDAPPROVIDERCLASS='{{ ofmLDAPProviderClass }}'
LDAPPROVIDERCONTROLFLAG='{{ ofmLDAPProviderControlFlag }}'
LDAPHOSTNAME='{{ ofmLDAPHostName }}'
LDAPHOSTPORT='{{ ofmLDAPHostPort }}'
LDAPHOSTPRINCIPAL='{{ ofmLDAPHostPrincipal }}'
LDAPHOSTCREDENTIAL='{{ ofmLDAPHostCredential }}'
LDAPBASEDN='{{ ofmLDAPBaseDN }}'
LDAPALLUSERSFILTER='{{ ofmLDAPAllUsersFilter }}'
LDAPUSERFROMNAMEFILTER='{{ ofmLDAPUserFromNameFilter }}'
LDAPUSERSEARCHSCOPE='{{ ofmLDAPUserSearchScope }}'
LDAPUSERNAMEATTRIBUTE='{{ ofmLDAPUserNameAttribute }}'
LDAPUSERNAMEOBJECTCLASS='{{ ofmLDAPUserNameObjectClass }}'
LDAPGROUPBASEDN='{{ ofmLDAPGroupBaseDN }}'
LDAPALLGROUPSFILTER='{{ ofmLDAPAllGroupsFilter }}'
LDAPGROUPFROMNAMEFILTER='{{ ofmLDAPGroupFromNameFilter }}'
LDAPGROUPSEARCHSCOPE='{{ ofmLDAPSearchScope }}'
LDAPGROUPMEMBERSHIPSEARCHING='{{ ofmLDAPGroupMembershipSearching }}'
LDAPGROUPMEMBERSHIPSEARCHLEVEL='{{ ofmLDAPGroupMembershipSearchLevel }}'
LDAPGROUPIGNOREDUPLICATEMEMBERSHIP='{{ ofmLDAPGroupIgnoreDuplicateMembership }}'
LDAPGROUPFROMUSERFILTERFORMEMBERIUD='{{ ofmLDAPGroupFromUserFilterForMemberUID }}'
LDAPSTATICGROUPOBJECTCLASS='{{ ofmLDAPStaticGroupObjectclass }}'
LDAPSTATICMEMBERDNATTRIBUTE='{{ ofmLDAPStaticMemberDNAttribute }}'
LDAPSTATICGROUPDNSFROMMEMBERDNFILTER='{{ ofmLDAPStaticGroupDNSFromMemberDNFilter }}'
LDAPDEFAULTAUTHENTICATORCONTROLFLAG='{{ ofmLDAPDefaultAuthenticatorControlFlag }}'


print 'Connecting to the '+ADMINSERVERNAME
connect(userConfigFile=USERHOMEDIR+'/bin/'+DOMAINNAME+'-cred.secure',userKeyFile=USERHOMEDIR+'/bin/'+DOMAINNAME+'-key.secure',url='t3://'+ADMINSERVERMACHINE+':'+ADMINSERVERPORT) 
edit()
startEdit()
try:
  print 'Configuring LDAP integration with provider '+LDAPPROVIDERNAME+' ('+LDAPHOSTNAME+')'
  cd('/SecurityConfiguration/'+DOMAINNAME+'/Realms/myrealm')
  cmo.createAuthenticationProvider(LDAPPROVIDERNAME,LDAPPROVIDERCLASS)
  cd('/SecurityConfiguration/'+DOMAINNAME+'/Realms/myrealm/AuthenticationProviders/'+LDAPPROVIDERNAME)
  cmo.setControlFlag(LDAPPROVIDERCONTROLFLAG)
  cmo.setHost(LDAPHOSTNAME)
  cmo.setPort(int(LDAPHOSTPORT))
  cmo.setPrincipal(LDAPHOSTPRINCIPAL)
  cmo.setCredential(LDAPHOSTCREDENTIAL)
  cmo.setUserBaseDN(LDAPBASEDN)
  cmo.setAllUsersFilter(LDAPALLUSERSFILTER)
  cmo.setUserFromNameFilter(LDAPUSERFROMNAMEFILTER)
  cmo.setUserSearchScope(LDAPUSERSEARCHSCOPE)
  cmo.setUserNameAttribute(LDAPUSERNAMEATTRIBUTE)
  cmo.setUserObjectClass(LDAPUSERNAMEOBJECTCLASS)
  cmo.setGroupBaseDN(LDAPGROUPBASEDN)
  cmo.setAllGroupsFilter(LDAPALLGROUPSFILTER)
  cmo.setGroupFromNameFilter(LDAPGROUPFROMNAMEFILTER)
  cmo.setGroupSearchScope(LDAPGROUPSEARCHSCOPE)
  cmo.setGroupMembershipSearching(LDAPGROUPMEMBERSHIPSEARCHING)
  cmo.setMaxGroupMembershipSearchLevel(int(LDAPGROUPMEMBERSHIPSEARCHLEVEL))
  cmo.setIgnoreDuplicateMembership(int(LDAPGROUPIGNOREDUPLICATEMEMBERSHIP))
  cmo.setGroupFromUserFilterForMemberuid(LDAPGROUPFROMUSERFILTERFORMEMBERIUD)
  cmo.setStaticGroupObjectClass(LDAPSTATICGROUPOBJECTCLASS)
  cmo.setStaticMemberDNAttribute(LDAPSTATICMEMBERDNATTRIBUTE)
  cmo.setStaticGroupDNsfromMemberDNFilter(LDAPSTATICGROUPDNSFROMMEMBERDNFILTER)
  cmo.setDynamicGroupObjectClass('')
  cmo.setDynamicMemberURLAttribute('')
  cmo.setDynamicGroupNameAttribute('')
  save()
  cd('/SecurityConfiguration/'+DOMAINNAME+'/Realms/myrealm/AuthenticationProviders/DefaultAuthenticator')
  cmo.setControlFlag(LDAPDEFAULTAUTHENTICATORCONTROLFLAG)
  save()
  activate()
except Exception, e:
  print e
  print 'LDAP configuration error! Undoing the changes!'
  undo(defaultAnswer='y', unactivatedChanges='true')
  stopEdit('y')
exit()