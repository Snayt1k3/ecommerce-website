function delete_product(id){
    var token = $('input[name=_token]').val();
    alertify.set('notifier','position', 'top-left');
    $.ajax({
        type: "POST",
        url: "/profile/seller/product/delete",
        data: {
            csrfmiddlewaretoken: token,
            'id': id,
            },
        dataType: "Json",
        success: function (response) {
            alertify.success(response['status'])
            
        }
    });
}