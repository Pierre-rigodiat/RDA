createBackup = function()
{
	var mongodbPath = $("#mongopath").val();
	Dajaxice.admin.createBackup(Dajax.process,{"mongodbPath":mongodbPath});
}

restoreBackup = function(backup)
{
	var mongodbPath = $("#mongopath").val();
	Dajaxice.admin.restoreBackup(Dajax.process,{"mongodbPath":mongodbPath,"backup":backup});
}

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