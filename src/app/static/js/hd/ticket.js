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
        $('#cat1-name').val(th.cat1_name);
        $('#cat2-name').val(th.cat2_name);
        $('#cat3-name').val(th.cat3_name);
    }


    function add_user_note(){
        let note_text = $('#hd_ticket_note').val();
        $.post($SCRIPT_ROOT + '/hd/_add_ticket_user_note', {
            ticket_id: ticket_id,
            note_text: note_text
        });
        $('#hd_ticket_note').val('');
        notify_params.className = 'success';
        $.notify('התיעוד נוסף בהצחה', notify_params);
        get_user_notes();
    }


    $('#add-user-note').on('click', add_user_note);


    function get_user_notes() {
        $.getJSON($SCRIPT_ROOT + '/hd/_get_ticket_user_notes', {
            'ticket_id': ticket_id
        }, function (tun) {
            $('.ticket_note').remove();
            $.each(tun, function(i, note) {
                tn = li_ticket_note.clone();
                tn.find('.main-text').html(note.note_text.replace(/\n/g, "<br />"));
                tn.find('.div-user-f-name').text(note.full_name);
                tn.find('.div-heb-date').text(note.time_ + ', ' +
                                                        note.heb_date);
                $('.ul_notes').append(tn.show())
            })
        });
    }


    get_ticket_header();

    li_ticket_note = $('.ticket_note').clone();
    get_user_notes();

});