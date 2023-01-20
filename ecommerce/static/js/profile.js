var btn = document.querySelector('.show_all_history');
var body = document.querySelector('.history_orders')
btn.addEventListener('click', function(){
    if (btn.innerHTML === 'Скрыть Историю'){
        btn.innerHTML = 'Показать Всю Историю';
        body.style.maxHeight = '500px';
    } else {
        btn.innerHTML = 'Скрыть Историю';
        body.style.maxHeight = 'None';
    };
});