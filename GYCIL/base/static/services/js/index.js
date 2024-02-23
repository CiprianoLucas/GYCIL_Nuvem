jQuery(function() {
    
    const $serviceModal = $("#serviceModal");
    const $budgetModal = $("#budgetModal");


    $serviceModal.on("show.bs.modal", function(e) {
        const $button = $(e.relatedTarget);

        const url = $button.data("url");

        fetch(url)
            .then(response => response.json())
            .then(service => {
                
                let descriptions;
                descriptions = service[0];
                
                const $serviceModalLabel = $("#serviceModalLabel");
                const $state_city = $("#state_city");
                const $street = $("#street");
                const $cep = $("#cep");
                const $client = $("#client");
                const $description = $("#description");
                const $created_at = $("#created_at");
                const $button_refuse = $("#button_refuse");
                const $button_accept = $("#button_accept");


                $serviceModalLabel.text(("SERVIÇO DE " + descriptions.category + ": " + descriptions.id).toUpperCase())
                $state_city.text(descriptions.state + " - " + descriptions.city);
                $street.text(descriptions.street);
                $cep.text(descriptions.cep);
                $client.text(descriptions.client)
                $description.text(descriptions.description);
                $created_at.text(descriptions.created_at.slice(0, 16));
                $button_refuse.attr("href", descriptions.url_refuse);
                $button_accept.attr("href", descriptions.url_accept);
       
                
            })
            .catch(console.error)
    });

    $budgetModal.on("show.bs.modal", function(e) {
        const $button = $(e.relatedTarget);

        const url = $button.data("url");

        fetch(url)
            .then(response => response.json())
            .then(budgets => {
                const $budgetTableBody = $("#budgetTableBody");
                $budgetTableBody.empty();

                

                budgets.forEach(budget => {
                    const $row = $('<tr></tr>');

                    const $buttonDescription = $('<button type="button" class="btn btn-secondary"><i class="bi bi-info-circle"></i></button>')
                    const $buttonReject = $('<button type="button" class="btn btn-danger ms-2 me-2"><i class="bi bi-ban"></i></button>')
                    const $buttonAccept = $('<button type="button" class="btn btn-success"><i class="bi bi-check"></i></button>')
                    
                    $optionButtons = $('<td></td>');
                    $optionButtons.append($buttonDescription)
                    $optionButtons.append($buttonReject)
                    $optionButtons.append($buttonAccept)

                    $row.append($("<td>").text(budget.company));
                    $row.append($("<td>").text(budget.price));
                    $row.append($("<td>").text(budget.date));
                    $row.append($optionButtons);

                    $budgetTableBody.append($row);
                })
                
            })
            .catch(console.error)
    });
    
});