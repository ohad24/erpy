$(document).ready(function() {

    function get_ticket_header() {
        $.getJSON($SCRIPT_ROOT + '/hd/_get_ticket_header', {
            'ticket_id': ticket_id
        }, function (th) {
            set_ticket_header(th);
        });
    }


    function set_ticket_header(th){
        $('#status-name').val(th.ticket_status_name);
        $('#open-date').val(th.open_date);
        $('#create-by-name').val(th.create_by_f_name);
        $('#hd-cat-1').val(th.cat1_id);
        $('#hd-cat-2').empty().append(new Option(th.cat2_name, th.cat2_id));
        $('#hd-cat-3').empty().append(new Option(th.cat3_name, th.cat3_id));
        $('#due-date').val(th.due_date);
        $('#assign-cust-by-name').val(th.assign_cust_name);
        $('#ticket-open-desc').html(th.open_note_desc);
        $('#team-names').empty();
        $.each( th.team_names, function( key, team_name ) {
            $('#team-names').append($('<li>').append(team_name))
        });
        if (th.ticket_status_id == 3){
            $('#close-by-name').val(th.close_by_f_name);
            $('#close-by-date').val(th.close_date);
            $('#close-reason-name').val(th.ticket_close_reason_name);
            $('#header-form-close-data').show();
            $('.close-element').hide();
            $('#header-edit-btn').remove();
        }
    }


    function edit_ticket_header(){
        $('#hd-cat-1').attr("disabled", false);
        $('#hd-cat-2').attr("disabled", false);
        $('#hd-cat-3').attr("disabled", false);
        $('#header-edit-btn').hide();
        $('#header-edit-btn-div').show();
    }

    $('#header-edit-btn').on('click', edit_ticket_header);


    function save_ticket_header() {
        hf = $('#header-form')[0];
        if (hf.checkValidity() === true) {
            $.post($SCRIPT_ROOT + '/hd/_set_ticket_header', {
                cat_3_id: $('#hd-cat-3').val(),
                ticket_id: ticket_id
            });
            reset_header()
        } else {
            hf.classList.add('was-validated');
        }
    }

    $('#header-save-btn').on('click', save_ticket_header);


    $('#header-cancel-btn').on('click', function () {
        reset_header()
    });


    function reset_header() {
        $('#header-form')[0].classList.remove('was-validated');
        $('#hd-cat-1').attr("disabled", true);
        $('#hd-cat-2').attr("disabled", true);
        $('#hd-cat-3').attr("disabled", true);
        get_ticket_header();
        $('#header-edit-btn').show();
        $('#header-edit-btn-div').hide();
    }


    function add_user_note(){
        let note_text = $('#hd_ticket_note').val();
        let close_reason_checked = $('#close-reason-cb').prop('checked');
        if ($('#hd_ticket_note').summernote('isEmpty') === false) {
            if (close_reason_checked) {
                let close_reason_id = $("#close-reason option:selected").val();
                if (close_reason_id != ""){
                    $.post($SCRIPT_ROOT + '/hd/_close_ticket', {
                        ticket_id: ticket_id,
                        note_text: note_text,
                        close_reason_id: close_reason_id
                    });
                    $('#hd_ticket_note').val('');
                    notify_params.className = 'success';
                    $.notify('הפניה נסגרה בהצלחה', notify_params);
                    setTimeout(function () {get_ticket_header();}, 750);
                    get_user_notes();
                }
            } else {
                $.post($SCRIPT_ROOT + '/hd/_add_ticket_user_note', {
                    ticket_id: ticket_id,
                    note_text: note_text
                });
                $('#hd_ticket_note').val('');
                notify_params.className = 'success';
                $.notify('התיעוד נוסף בהצחה', notify_params);
                get_user_notes();
            }
            $('#hd_ticket_note').summernote('reset');
        }
    }


    $('#add-user-note').on('click', add_user_note);


    function get_user_notes() {
        $.getJSON($SCRIPT_ROOT + '/hd/_get_ticket_user_notes', {
            'ticket_id': ticket_id
        }, function (tun) {
            $('.ticket_note').remove();
            $.each(tun, function(i, note) {
                tn = li_ticket_note.clone();
                tn.find('#main-text').html(note.note_text.replace(/\n/g, "<br />"));
                tn.find('#ticket-type-name').text(note.ticket_note_type_name);
                tn.find('#div-user-f-name').text(note.full_name);
                tn.find('#div-heb-date').text(note.time_ + ', ' +
                                                        note.heb_date);
                $('.ul_notes').append(tn.show())
            })
        });
    }


    function get_user_files() {
        $.getJSON($SCRIPT_ROOT + '/hd/_get_ticket_user_files', {
            'ticket_id': ticket_id
        }, function (tuf) {
            $.each(tuf, function(i, tuf) {
                a = $("<a/>")
                    .attr("href", $SCRIPT_ROOT + '/hd/users_files/' + tuf.gen_file_name)
                    .html($("<dbi/>").text(tuf.file_name));
                div = $("<div/>").addClass('text-truncate');
                $('#files-div').append(div.append(a))
            })
        });
    }


    $('#close-reason-cb').on('click', function () {
        let checked = $(this).prop('checked');
        if (checked) {
            $("#close-reason").val($("#close-reason option:first").val());
            $('#close-reason-div').show();
        } else {
            $('#close-reason-div').hide()
        }
    });


    get_ticket_header();
    li_ticket_note = $('.ticket_note').clone();
    get_user_notes();
    get_user_files();

});