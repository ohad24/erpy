$(document).ready(function() {

    $("#hd_ticket_multi_file").bind('change', function(){
        if (this.files.length > 3) {
            $("#hd_ticket_multi_file").val('');
            alert('לא יותר מ 3 קבצים');
        }
        $.each( this.files, function( key, file ) {
            console.log(file.name);
            console.log((file.size / 1024 / 1024).toPrecision(1));
            if ((file.size / 1024 / 1024).toPrecision(1) > 5) {
                $("#hd_ticket_multi_file").val('');
                alert('כל קובץ עד 5 מגה');
            }
            // files_names.push(file.name + ' (' +
            // (file.size / 1024 / 1024).toPrecision(1) + 'MB)')
        });

    });

});