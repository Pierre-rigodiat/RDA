<?php
/**
 * Configuration file of modules
 */
// TODO Use the session storage
$modules = array(
	/* --- HOW TO REGISTER YOUR MODULE ---
	 *
	 * Register all your module here. The syntax is the following:
	 *
	 * 		'#moduleFolderName#' => array(
	 * 			'class' => '#moduleClassName#',
	 * 			'published' => #true/false#
	 * 		)
	 *
	 * All element surrounding by the # sign must be edited and replaced by your module property.
	 * The 'published' boolean only tell the admin that a module is in development and will
	 * soon be integrated to the website
	 */
	// TABLE MODULE
	'hdf5Table' => array(
		'name' => 'Excel tables',
		'class' => 'Table',
		'published' => true
	),

	// PERIODIC TABLE MODULE
	'periodicTable' => array(
		'name' => 'Periodic table',
		'class' => 'PeriodicTable',
		'published' => false

	),

	// IMAGE MODULE
	'images' => array(
		'class' => 'Images',
		'published' => false
	),

	// QUERY TABLE MODULE
	'queryTable' => array(
			'name' => 'Query Table',
			'class' => 'QueryTable',
			'published' => false
	)
);
?>