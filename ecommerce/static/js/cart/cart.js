// Добавление Товара В Корзину
function add_to_cart(id){
    alertify.set('notifier','position', 'top-left');
    var token = $('input[name=_token]').val();
    $.ajax({
        type: "POST",
        url: "/cart/add_to_cart",
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
        url: "/cart/minus_quantity",
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


// Удаление Товара из Корзины
function delele_from_cart(id){
    alertify.set('notifier','position', 'top-left');
    var token = $('input[name=_token]').val();
    $.ajax({
        type: "POST",
        url: "/cart/delete_from_cart",
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