$(document).ready(function() {

    function update_child_cat_field(cat_level, hd_category_id) {
        let cat_select_id_name =  '#hd_cat_' + cat_level;
        $(cat_select_id_name)
            .empty()
            .append("<option selected value disabled> -- ללא -- </option>");
        if (cat_level == 2) {
            $('#hd_cat_3')
            .empty()
            .append("<option selected value disabled> -- ללא -- </option>");
        }
        $.getJSON($SCRIPT_ROOT + '/hd/_get_children_category', {
            'cat_id': hd_category_id,
            'cat_level': cat_level
            }, function (data) {
                $.each(data, function( index, value ) {
                    $(cat_select_id_name)
                        .append(new Option(value.category_name, value.id));
                });
            }
            )
        }

    $('#hd_cat_1').change({'cat_level': 2},
        function(event) {
            let hd_category_id = $('#hd_cat_1').val();
            update_child_cat_field(event.data.cat_level, hd_category_id)
    });
    $('#hd_cat_2').change({'cat_level': 3},
        function(event) {
            let hd_category_id = $('#hd_cat_2').val();
            update_child_cat_field(event.data.cat_level, hd_category_id)
    });
    // $('#hd_cat_2').on('change', update_child_cat_field, {cat_level: 3});

    // update_parent_field();

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