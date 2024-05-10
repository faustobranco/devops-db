gitlab_rails['ldap_enabled'] = true
gitlab_rails['ldap_servers'] = {
'main' => {
  'label' => 'Devops-db',
  'host' =>  'ldap.devops-db.info',
  'port' => 636,
  'uid' => 'uid',
  'bind_dn' => 'cn=readonly-bind-dn,ou=ServiceGroups,dc=ldap,dc=devops-db,dc=info',
  'password' => '1234qwer',
  'encryption' => 'simple_tls',
  'verify_certificates' => false,
  'active_directory' => false,
  'lowercase_usernames' => 'false',
  'retry_empty_result_with_codes' => [80],
  'allow_username_or_email_login' => false,
  'base' => 'dc=ldap,dc=devops-db,dc=info',
  'tls_options' => {
    'ca_file' => '/etc/ssl/certs/ldapcacert.crt',
    'ssl_version' => 'TLSv1_2'  
    },
  'user_filter' => '(&(objectClass=person)(memberOf=cn=GitLabGroup,ou=SecurityGroups,dc=ldap,dc=devops-db,dc=info))'
  }
}
