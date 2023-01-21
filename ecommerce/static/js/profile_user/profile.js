var btn = document.querySelector('.show_all_history');
var btn1 = document.querySelector('.show_all_chistory');
var body = document.querySelector('.history_orders');
var body1 = document.querySelector('.current_orders');
var email_sent_btn = document.querySelector('.email_btn');

btn.addEventListener('click', function(){
    if (btn.innerHTML === 'Скрыть Историю'){
        btn.innerHTML = 'Показать Всю Историю';
        body.style.maxHeight = '500px';
    } else {

        btn.innerHTML = 'Скрыть Историю';
        body.style.maxHeight = 'None';
    };
});


btn1.addEventListener('click', function(){
    if (btn1.innerHTML === 'Скрыть Историю'){
        btn1.innerHTML = 'Показать Всю Историю';
        body1.style.maxHeight = '500px';
    } else {
        btn1.innerHTML = 'Скрыть Историю';
        body1.style.maxHeight = 'None';
    };
});

email_sent_btn.addEventListener('click', function(){
    var email_conf_div = document.querySelector('.email_confirm_div');
    var token = $('input[name=_token]').val();
    alertify.set('notifier','position', 'top-left');
    $.ajax({
        type: "POST",
        url: "/profile/email/send",
        data: {csrfmiddlewaretoken: token},
        dataType: "json",
        success: function (response) {
            if (response['error']){
                alertify.error(response['status']);
            } else{
                alertify.success(response['status']);
                email_conf_div.classList.remove('invisible');
                email_sent_btn.classList.add('invisible');
            };
        }
    });

    var email_confirm_btn = document.querySelector('.sent_btn_key');
    email_confirm_btn.addEventListener('click', function(){
        var auth_key = $('input[name=auth_email_key]').val();
        var token = $('input[name=_token]').val();
        $.ajax({
            type: "POST",
            url: "/profile/email/confirm",
            data: {'auth_key': auth_key,
                    csrfmiddlewaretoken: token
            },
            dataType: "json",
            success: function (response) {
                location.reload();

            }
        });
    })
});