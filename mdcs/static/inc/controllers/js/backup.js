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
	create_backup();
}


/**
 * AJAX call, creates a backup
 */
create_backup = function(){
    $.ajax({
        url : "/admin/create_backup",
        type : "GET",
        dataType: "json",        
        success: function(data){
        	$("#backup-message").html(data.result);
            showBackupDialog();
        }
    });
}


/**
 * Restore a backup to the running mongodb instance.
 */
restoreBackup = function(backup)
{
	restore_backup(backup);
}


/**
 * AJAX call, restore a backup
 * @param backup
 */
restore_backup = function(backup){
    $.ajax({
        url : "/admin/restore_backup",
        type : "POST",
        dataType: "json",
        data : {
        	backup : backup,
        },
        success: function(data){
        	$("#backup-message").html(data.result);
            showBackupDialog();
        }
    });
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
                	delete_backup(backup);
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
 * AJAX call, delete a backup
 * @param backup
 */
delete_backup = function(backup){
    $.ajax({
        url : "/admin/delete_backup",
        type : "POST",
        dataType: "json",
        data : {
        	backup : backup,
        },
        success: function(data){
        	$('#model_selection').load(document.URL +  ' #model_selection', function() {});
        }
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
