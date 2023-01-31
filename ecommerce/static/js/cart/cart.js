// Добавление Товара В Корзину
function add_to_cart(id){
    alertify.set('notifier','position', 'top-left');
    let token = $('input[name=_token]').val();
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
    let token = $('input[name=_token]').val();
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
    let token = $('input[name=_token]').val();
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

function promo_activate(value){
    let token = $('input[name=_token]').val();
    let valid_feed = document.querySelector('.valid-feedback');
    let invalid_feed = document.querySelector('.invalid-feedback');

    $.ajax({
        type: "POST",
        url: "/cart/promo_activate",
        data: {
            csrfmiddlewaretoken: token,
            'promo': value,
        },
        dataType: "json",
        success: function (response) {
            if (response['error']){
                invalid_feed.innerHTML = response['status'];
                invalid_feed.style.display = 'block';
                valid_feed.style.display = 'none'
            } else {
                valid_feed.innerHTML = response['status'];
                valid_feed.style.display = 'block';
                invalid_feed.style.display = 'none'
                
                let price = document.querySelector('.total-price');

                if (response['promo']['is_percent']){
                        price.innerHTML =  (parseInt(price.textContent) * (response['promo']['amount_of_discount'] / 100)) + 'руб'
                } else {
                    price.innerHTML = (parseInt(price.textContent) - response['promo']['amount_of_discount']) + 'руб'
                }
            };
            
        }
    });
};


function promo_clear(value){
    alertify.set('notifier','position', 'top-left');
    let token = $('input[name=_token]').val();
    let valid_feed = document.querySelector('.valid-feedback');
    let invalid_feed = document.querySelector('.invalid-feedback');
    let price = document.querySelector('.total-price');

    document.getElementById('promo').value = '';
    invalid_feed.style.display = 'none'
    valid_feed.style.display = 'none'
    price.innerHTML = value + 'руб'
    $.ajax({
        type: "POST",
        url: "/cart/promo_delete",
        data: {csrfmiddlewaretoken: token,},
        dataType: "json",
        success: function (response) {
            alertify.success(response['status'])
        }
    });
}