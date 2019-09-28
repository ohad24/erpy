$(document).ready(function() {

    function update_parent_field() {
        let hd_category_level = $('#hd_category_level').val();
        if (hd_category_level == 1) {
            $('#fg_hd_category_parent_id').hide();
            $('#hd_category_parent_id').prop('required',false);
        } else {
            $('#fg_hd_category_parent_id').show();
            $('#hd_category_parent_id').prop('required',true);
            $.getJSON($SCRIPT_ROOT + '/hd/_update_select_category', {
                'hd_category_level': $('#hd_category_level').val()
                }, function (data) {
                    $("#hd_category_parent_id")
                        .empty()
                        .append("<option selected value disabled> -- ללא -- </option>");
                    $.each(data, function( index, value ) {
                        $("#hd_category_parent_id")
                            .append(new Option(value.category_name, value.id));
                    });
                });
            }
        }

    $('#hd_category_level').on('change', update_parent_field);

    update_parent_field();

});