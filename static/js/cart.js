var updateBtns = document.getElementsByClassName('update-cart')

for(var i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.book
        var action = this.dataset.action
        var qty = this.dataset.qty
        updateUserOrder(productId, action, qty)
        updatecartcount()
    })
}

function updateUserOrder(productId, action, qty) {
    $.ajax({  
        url: '/update-item',  
        type: 'POST',  
        data: { 
            'productId': productId,
            'action': action,
            'quantity': qty,
            csrfmiddlewaretoken: csrf_token,
        },
        dataType: 'json',  
        success: function(data, textStatus, xhr) {  
            $('#cart_count').text(data.total)
        },  
        error: function(xhr, textStatus, errorThrown) {  
          console.log(textStatus);   
        }  
    });  
}

$(document).ready(updatecartcount);

function updatecartcount() {
    $.ajax({  
        url: '/update-item',  
        type: 'GET',  
        dataType: 'json',  
        success: function(data, textStatus, xhr) {  
            $('*[id*=cart-total]').each(function() {
                $(this).text(data.total);
            });
        },  
        error: function(xhr, textStatus, errorThrown) {  
            console.log(textStatus);   
        }  
    }); 
    
    updateTotal()
}

function updateTotal(){
    var all = $(".bill-amount").map(function() {
        return this.innerHTML;
    }).get();
    
    total = 0
    for(var i=0; i<all.length; i++){
        total += parseFloat(all[i].substring(1))
    }
    $('*[id*=total-bill]').each(function() {
        $(this).html('$'+total.toFixed(2));
    });
}

var deleteBtn = document.getElementsByClassName('remove-from-cart')

for(var i=0; i<deleteBtn.length; i++){
    deleteBtn[i].addEventListener('click', function () {
        var productId = this.dataset.book
        var qty = this.dataset.quantity
        updateUserOrder(productId, 'remove', qty)
        $(this).closest('tr').remove()
        updatecartcount()
    })
}


var inputFields = document.getElementsByClassName('item-quantity')
for(var i=0; i<inputFields.length; i++){
    inputFields[i].addEventListener('change', function () {
        var price = this.dataset.price
        var updated_qty = this.value

        
        $(this).closest('td').siblings('.total').html('<strong class="woocommerce-Price-amount amount bill-amount">$'+parseFloat(price*updated_qty).toFixed(2)+'</strong>')
        
    })
}

var inputFields = document.getElementsByClassName('js-minus')
for(var i=0; i<inputFields.length; i++){
    inputFields[i].addEventListener('click', function () {
        var next = $(this).nextAll(".item-quantity");
        var qty = next[0].value;
        var price = next[0].dataset.price
        var updated_qty = qty - 1
        next[0].value = updated_qty
        
        $(this).closest('td').siblings('.total').html('<strong class="woocommerce-Price-amount amount bill-amount">$'+parseFloat(price*updated_qty).toFixed(2)+'</strong>')
        
    })
}

var inputFields = document.getElementsByClassName('js-plus')
for(var i=0; i<inputFields.length; i++){
    inputFields[i].addEventListener('click', function () {
        var next = $(this).prevAll(".item-quantity");
        var qty = parseInt(next[0].value);
        var price = next[0].dataset.price
        var updated_qty = qty + 1
        next[0].value = updated_qty
        
        $(this).closest('td').siblings('.total').html('<strong class="woocommerce-Price-amount amount bill-amount">$'+parseFloat(price*updated_qty).toFixed(2)+'</strong>')
        
    })
}
