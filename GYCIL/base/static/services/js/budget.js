jQuery(function() {

    const $inputDate = $("#id_date");
    const $inputHours = $("#id_hours_service");
    const $inputPrice = $("#id_price");
    
    
    $inputPrice.mask("000.000.000.000.000,00", {reverse: true});
    $inputDate.mask("00/00/0000");
    $inputHours.mask("00:00");
    
    const $send_button = $("#send_button");
    
})