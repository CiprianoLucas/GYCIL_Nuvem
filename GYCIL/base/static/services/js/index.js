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
                const $status = $("#status");
                const $date_start = $("#date_start");
                const $hours_service = $("#hours_service");
                const $company = $("#company");
                const $price = $("#price");
                const $button_refuse = $("#button_refuse");
                const $button_accept = $("#button_accept");
                const $button_delete = $("#button_delete");

                if (descriptions.status === "Aceito"){
                    $button_accept.text("Finalizar")
                }
                else if (descriptions.status == "Aguardando avaliação" ||
                         descriptions.status == "Concluido"){
                    $button_accept.remove()
                    $button_refuse.remove()
                    $button_delete.remove()
                }

                console.log(descriptions.status)
                

                $serviceModalLabel.text(("SERVIÇO DE " + descriptions.category + ": " + descriptions.id).toUpperCase())
                $state_city.text(descriptions.state + " - " + descriptions.city);
                $street.text(descriptions.street);
                $cep.text(descriptions.cep);
                $client.text(descriptions.client)
                $description.text(descriptions.description);
                $created_at.text(descriptions.created_at.slice(0, 16));
                $status.text(descriptions.status);
                $date_start.text(descriptions.date_start);
                $hours_service.text(descriptions.hours_service);
                $company.text(descriptions.company);
                $price.text(descriptions.price);
                $button_refuse.attr("href", descriptions.url_refuse);
                $button_accept.attr("href", descriptions.url_accept);
                $button_delete.attr("href", descriptions.url_delete);
       
                
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

                    const $buttonDescription = $('<a href="" type="button" class="btn btn-secondary"><i class="bi bi-info-circle"></i></a>')
                    const $buttonReject = $('<a href="" type="button" class="btn btn-danger ms-2 me-2"><i class="bi bi-ban"></i></a>')
                    const $buttonAccept = $('<a href="" type="button" class="btn btn-success"><i class="bi bi-check"></i></a>')

                    $buttonAccept.attr("href", budget.url_accept);
                    $buttonDescription.attr("href", budget.budget_file);
                    $buttonReject.attr("href", budget.url_refuse);
                    
                    const $buttons = $('<div class="d-grid gap-2"></div>')
                    $buttons.append($buttonDescription)
                    $buttons.append($buttonReject)
                    $buttons.append($buttonAccept)
                    
                    const $optionButtons = $('<td></td>');
                    $optionButtons.append($buttons)

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