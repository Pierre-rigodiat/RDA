<?php
$ldap_ip='129.6.59.30';
$ldap_dc=array('nist','gov');

$ldap_uid='pnd';
$ldap_pwd='021188';

/* Connection */
$ds = ldap_connect($ldap_ip);
ldap_set_option($ds, LDAP_OPT_PROTOCOL_VERSION, 3);

if(!$ds)
	throw new Exception("ldap_connect error");

echo 'Connected to LDAP<br/>';

/* Building useful variables */
$ldap_dn = '';
foreach ($ldap_dc as $dc_entry)
{
	$ldap_dn .= 'dc='.$dc_entry;

	if(end($ldap_dc)!=$dc_entry) $ldap_dn.=',';
}

$searchResult = ldap_search($ds, $ldap_dn, 'uid='.$ldap_uid);
$entries = ldap_get_entries($ds, $searchResult);

if($entries['count']!=1)
	throw new Exception("Invalid login");

echo 'User found: '.$entries[0]['dn'].'<br/>';

if(!ldap_bind($ds, $entries[0]['dn'], $ldap_pwd))
	throw new Exception("ldap_bind error");

echo 'Password OK';
ldap_unbind($ds);
