$(document).ready(function() {

    function update_modal_data() {
        let ticket_id = $(this).parent().parent()
                            .find('th')
                            .find('a').text();
        let ticket_desc = $(this).val();
        $('.modal-body').html(ticket_desc);
        $('#model-title-ticket-id').html(ticket_id);
    }

    $('.ticket-desc').on('click', update_modal_data);

});