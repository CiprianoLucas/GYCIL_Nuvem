jQuery(function() {

    const $inputPrice = $("#id_price");
    const $inputDate = $("#id_date");
    const $inputHours = $("#id_hours_service");

    
    $inputPrice.mask("000.000.000.000.000,00", {reverse: true});
    $inputDate.mask("00/00/0000");
    $inputHours.mask("00:00");

})