window.onload = function () {
/*
    // можем получить DOM-объект меню через JS
    var menu = document.getElementsByClassName('basket_record')[0];
    menu.addEventListener('click', function (event) {
        console.log(event);
        event.preventDefault();
    });

    // можем получить DOM-объект меню через jQuery
    $('.basket_record').on('click', 'img', function (event) {
        console.log('event', event);
        console.log('this', this);
        console.log('event.target', event.target);
        event.preventDefault();
    });
    // получаем атрибут href
    $('.basket_record').on('click', 'a', function (event) {
        var target_href = event.target.href;
        if (target_href) {
            console.log('нужно перейти: ', target_href);
        }
        event.preventDefault();
    });

*/
    // добавляем ajax-обработчик для обновления количества товара
    $('.orders_list').on('click', '.menu-link', function (event) {
        let target_href = event.target;
        console.log('hello')
        if (target_href) {
            $.ajax({
                url: "/admin/orders/read/" + target_href.name + "/" + target_href.innerText + "/",

                success: function (data) {
                    $('.orders_list').html(data.result);
                    console.log('ajax done');
                },
            });

        }
        event.preventDefault();
    });

};