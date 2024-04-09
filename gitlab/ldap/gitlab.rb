gitlab_rails['ldap_enabled'] = true
gitlab_rails['ldap_servers'] = {
'main' => {
  'label' => 'Devops-db',
  'host' =>  'ldap.devops-db.info',
  'port' => 389,
  'uid' => 'uid',
  'encryption' => 'plain',
  'verify_certificates' => false,
  'bind_dn' => 'cn=admin,dc=devops-db,dc=info',
  'password' => 'JbBmKx#lK@ZX4*amqd5l',
  'active_directory' => false,
  'lowercase_usernames' => 'false',
  'retry_empty_result_with_codes' => [80],
  'allow_username_or_email_login' => false,
  'base' => 'ou=UserGroups,dc=devops-db,dc=info',
  'user_filter' => '(&(objectClass=person)(memberOf=cn=GitLabGroup,ou=SecurityGroups,dc=devops-db,dc=info))'
  }
}