document.addEventListener('DOMContentLoaded', function(){
    alertify.set('notifier','position', 'top-left');
    var add_btns = this.querySelectorAll('.AddToCart');
    var products_id = this.querySelectorAll('.prod_id');
    var token = $('input[name=_token]').val();
    for (var i = 0; i < add_btns.length; i++){
        var current_btn = add_btns[i];
        var current_id = products_id[i];
        current_btn.addEventListener('click', function(){
            var id = $(current_id).val();
            $.ajax({
                type: "POST",
                url: "/add_to_cart",
                data: {
                    'prod_id': id,
                    csrfmiddlewaretoken: token
                },
                dataType: "json",
                success: function (response) {
                    alertify.success(response['status'])
                    
                }
            });
        })
    }
});