/**
 * Create a backup of the running mongodb instance.
 */
createBackup = function()
{
	var mongodbPath = $("#mongopath").val();
	Dajaxice.admin.createBackup(Dajax.process,{"mongodbPath":mongodbPath});
}

/**
 * Restore a backup to the running mongodb instance.
 */
restoreBackup = function(backup)
{
	var mongodbPath = $("#mongopath").val();
	Dajaxice.admin.restoreBackup(Dajax.process,{"mongodbPath":mongodbPath,"backup":backup});
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