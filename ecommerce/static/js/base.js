// Добавление В список желаемого
function add_to_wish(id){
    alertify.set('notifier','position', 'top-left');
    var token = $('input[name=_token]').val();
    $.ajax({
        type: "POST",
        url: "/add_to_wish",
        data: {
            'product_id': id,
            csrfmiddlewaretoken: token
        },
        dataType: "json",
        success: function (response) {
            alertify.success(response['status']);
            
        },
    });
}

// Удаление из списка жедаемого
function delete_from_wish(id){
    alertify.set('notifier','position', 'top-left');
    var token = $('input[name=_token]').val();
    $.ajax({
        type: "POST",
        url: "/delete_from_wish",
        data: {
            'product_id': id,
            csrfmiddlewaretoken: token
        },
        dataType: "json",
        success: function (response) {
            alertify.success(response['status']);
            setTimeout(()  =>{location.reload()}, 2000);
            
            
        },
        error: function(response){
            alertify.error(response['status'])
        }
    });
}
