document.addEventListener('DOMContentLoaded', function(){
    var btnwish = document.querySelector('.AddToWishList');
    alertify.set('notifier','position', 'top-right');
    btnwish.addEventListener('click', function(){
        var prod_id = $('.prod_id').val();
        var token = $('input[name=_token]').val();
        $.ajax({
            type: "POST",
            url: "/add_to_wish",
            data: {
                'product_id': prod_id,
                csrfmiddlewaretoken: token
            },
            dataType: "json",
            success: function (response) {
                console.log(response);
                alertify.success(response['status']);
                
            },
            error: function(response){
                console.log(response);
                alertify.error(response['status'])
            }
        });
    })
})
