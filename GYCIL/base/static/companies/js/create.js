$(document).ready(function(){

    const $zipcodeInput = $("#id_zipcode");
    const $streetInput = $("#id_street");
    const $numberInput = $("#id_number");
    const $cityInput = $("#id_city");
    const $stateInput = $("#id_state");
    const $cnpjInput = $("#id_cnpj");
    const $phoneInput = $("#id_phone");


    $cnpjInput.mask('00.000.000/0000-00');
    $zipcodeInput.mask('00000-000')
    $phoneInput.mask('(00) 00000-0000')

    $zipcodeInput.on("blur", function () {
        
        const zipcode = $(this).val().replace("-", "");

        if (zipcode.length !== 8) return;

        fetch(`https://viacep.com.br/ws/${zipcode}/json/`)
            .then(res => res.json()) // Obtendo somento os dados da requisição
            .then(data => {
                if (!data.erro) { 
                    $streetInput.val(data.logradouro);
                    $cityInput.val(data.localidade);
                    $stateInput.val(data.uf);

                    $numberInput.focus();
                }
            })
            .catch(() => console.error("Falha ao realizar a requisição para a API do VIACEP"))
            .finally(() => $zipcodeIcon.attr("class", "bi bi-geo-alt"));
    });


});