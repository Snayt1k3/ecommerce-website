

// Добавление Товара В Корзину
function add_to_cart(id){
    alertify.set('notifier','position', 'top-left');
    var token = $('input[name=_token]').val();
    $.ajax({
        type: "POST",
        url: "/add_to_cart",
        data: {
            'product_id':id,
            csrfmiddlewaretoken: token
        },
        dataType: "json",
        success: function (response) {
            alertify.success(response['status'])
        }
    });
}

// Уменьшение Кол-ва Товара В Корзине
function minus_quantity(id){
    alertify.set('notifier','position', 'top-left');
    var token = $('input[name=_token]').val();
    $.ajax({
        type: "POST",
        url: "/minus_quantity",
        data: {
            'product_id': id,
            csrfmiddlewaretoken: token
        },
        dataType: "json",
        success: function (response) {
            alertify.success(response['status']);
            setTimeout(()  =>{location.reload()}, 2000);
             
        }
    })
}

// Увеличение Кол-ва Товара В Корзине
function plus_quantity(id){
    alertify.set('notifier','position', 'top-left');
    var token = $('input[name=_token]').val();
    $.ajax({
        type: "POST",
        url: "/plus_quantity",
        data: {
            'product_id': id,
            csrfmiddlewaretoken: token
        },
        dataType: "json",
        success: function (response) {
            alertify.success(response['status']);
            setTimeout(()  =>{location.reload()}, 2000);
        }
    });
}

// Удаление Товара из Корзины
function delele_from_cart(id){
    alertify.set('notifier','position', 'top-left');
    var token = $('input[name=_token]').val();
    $.ajax({
        type: "POST",
        url: "/delete_from_cart",
        data: {
            'product_id': id,
            csrfmiddlewaretoken: token
        },
        dataType: "json",
        success: function (response) {
            alertify.success(response['status']);
            setTimeout(()  =>{location.reload()}, 2000);
        }
    });

}

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
