var btn = document.querySelector('.show_all_history');
var btn1 = document.querySelector('.show_all_chistory');
var body = document.querySelector('.history_orders');
var body1 = document.querySelector('.current_orders');


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