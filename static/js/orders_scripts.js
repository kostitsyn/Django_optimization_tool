'use strict';

window.onload = function() {
    let quantity_arr = [];
    let price_arr = [];

    let TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    var order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    var order_total_cost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;

    for (let i=0; i < TOTAL_FORMS; i++){
        let _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        let _price = (parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'))).toFixed(2);
        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        }else {
            price_arr[i] = 0;
        }
    }

    if (!order_total_quantity) {
        for (let i=0; i < TOTAL_FORMS; i++) {
            order_total_quantity += quantity_arr[i];
            order_total_cost += quantity_arr[i] * price_arr[i];
        }
        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(Number(order_total_cost.toFixed(2).toString()));
    }

    $('.order_form').on('click keyup', 'input[type="number"]', function (event) {

        let target = event.target;
        let orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));

        if (price_arr[orderitem_num]) {
            let orderitem_quantity = parseInt(target.value);

            let current_tr = $('tr').eq(orderitem_num + 1);
            let quantity_storage = parseInt(current_tr.find('td:eq(3)')[0].innerText);

            $(target).attr('max', quantity_storage);

            if (quantity_storage >= orderitem_quantity) {

                var delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
                quantity_arr[orderitem_num] = orderitem_quantity;
            }else {
                delta_quantity = 0;
                quantity_arr[orderitem_num] = quantity_storage;
            }
            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
        }
    });


    $('.order_form').on('click', 'input[type="checkbox"]', function(event) {

        let target = event.target;
        let orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));

        if (target.checked) {
            var delta_quantity = -quantity_arr[orderitem_num];
        }else {
            var delta_quantity = quantity_arr[orderitem_num];
        }
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    });

    $('.order_form select').change(function(event) {
    // $('.order_form').on('change', 'select', function(event) {
        let target = event.target;
        let orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
        let orderitem_product_pk = target.options[target.selectedIndex].value;

        if (orderitem_product_pk) {
            $.ajax({
                url: "/order/product/" + orderitem_product_pk + "/price/",
                success: function (data) {
                    if (data.price) {
                        price_arr[orderitem_num] = parseFloat(data.price);
                        if (isNaN(quantity_arr[orderitem_num])) {
                            quantity_arr[orderitem_num] = 0;
                        }
                        let price_html = '<span>' + data.price.toString().replace('.', ',') + '</span>';
                        let current_tr_price = $('.order_form table').find('tr:eq(' + (orderitem_num + 1) + ')');
                        current_tr_price.find('td:eq(2)').html(price_html);

                        let quantity_storage = '<span>' + data.quantity_storage.toString() + '</span>';
                        let current_tr_quantity = $('.order_form table').find('tr:eq(' + (orderitem_num + 1) + ')');
                        current_tr_quantity.find('td:eq(3)').html(quantity_storage);
                        if ((current_tr_price.find('input[type="number"]').val()) === '') {
                            current_tr_price.find('input[type="number"]').val(0);
                        }
                        orderSummaryRecalc();

                    }
                },
            });
        }
    });

    function orderSummaryRecalc() {
        order_total_quantity = 0;
        order_total_cost = 0;

        for (let i=0; i < TOTAL_FORMS; i++) {
            order_total_quantity += quantity_arr[i];
            order_total_cost += quantity_arr[i] * price_arr[i];
        }
        $('.order_total_cost').html(order_total_cost.toFixed(2).toString().replace('.', ','));
        $('.order_total_quantity').html(order_total_quantity.toString());
    }

    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        let delta_cost = orderitem_price * delta_quantity;

        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;

        $('.order_total_cost').html((order_total_cost.toFixed(2).toString().replace('.', ',')));
        $('.order_total_quantity').html(order_total_quantity.toString());
    }

    $('.formset_row').formset( {
        addText: 'добавить товар',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem,
    });

    function deleteOrderItem(row) {
        let target_name = row[0].querySelector('input[type="number"]').name;
        let orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
        let delta_quantity = -quantity_arr[orderitem_num];
        quantity_arr[orderitem_num] = 0;
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    }
}