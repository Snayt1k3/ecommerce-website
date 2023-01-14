document.addEventListener('DOMContentLoaded', function(){
    alertify.set('notifier','position', 'top-right');
    var del_btn = document.querySelectorAll('.deleteBtnWl');
    var id_products = document.querySelectorAll('.prod_id');
    var token = $('input[name=_token]').val();
    if (del_btn){
        for (var i = 0; i < del_btn.length; i++){
            var current_btn = del_btn[i];
            var current_id = $(id_products[i]).val();
            console.log(current_btn, current_id, token);
            current_btn.addEventListener('click', function(){
                $.ajax({
                    type: "POST",
                    url: "delete_from_wish",
                    data: {
                        'prod_id': current_id,
                        csrfmiddlewaretoken: token
                    },
                    dataType: "json",
                    success: function (response) {
                        alertify.success(response['status']);
                        location.reload(1000);
                        
                    },
                    error: function(response){
                        console.log(response);
                        alertify.error(response['status'])
                    }
                });
            })
        }

    }
})