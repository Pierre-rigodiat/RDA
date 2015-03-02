/**
 * 
 * File Name: backup.js
 * Author: Sharief Youssef
 * 		   sharief.youssef@nist.gov
 *
 *        Guillaume SOUSA AMARAL
 *        guillaume.sousa@nist.gov
 * 
 * Sponsor: National Institute of Standards and Technology (NIST)
 * 
 */


/**
 * Create a backup of the running mongodb instance.
 */
createBackup = function()
{
	Dajaxice.admin.createBackup(Dajax.process);
}

/**
 * Restore a backup to the running mongodb instance.
 */
restoreBackup = function(backup)
{
	Dajaxice.admin.restoreBackup(Dajax.process,{"backup":backup});
}

/**
 * Delete a backup.
 */
deleteBackup = function(backup)
{
	$(function() {
        $( "#dialog-delete-backup" ).dialog({
            modal: true,
            width: 520,
            buttons: {
                Delete: function() {    
                	Dajaxice.admin.deleteBackup(Dajax.process,{"backup":backup});
                    $( this ).dialog( "close" );
                    },
                Cancel: function() {    
                    $( this ).dialog( "close" );
                    },
            }      
        });
    });
}

/**
 *	Open a dialog with the status of the backup command
 */
showBackupDialog = function(){
    $(function() {
        $( "#dialog-backup" ).dialog({
            modal: true,
            width: 520,
            buttons: {
                OK: function() {    
                    $( this ).dialog( "close" );
                    }
            }      
        });
    });
    $('#model_selection').load(document.URL +  ' #model_selection', function() {});
}
