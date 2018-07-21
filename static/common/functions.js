

function addcart(id){
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()

    $.ajax({
        url:'/axf/addtocart/',
        type:'POST',
        dataType:'json',
        data:{'good_id':id},
        headers:{'X-CSRFToken':csrf},
        success:function(data){
            if(data['code'] == '200'){
                $('#good_' + id).html(data['c_num'])
            }
        },
        error:function(data){
            alert('失败')
        }

    });
}


function subcart(id){
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()

    $.ajax({
        url:'/axf/subtocart/',
        type:'POST',
        data:{'good_id':id},
        headers:{'X-CSRFToken':csrf},
        dataType:'json',
        success:function(data){
            if(data['code'] == '200'){
                $('#good_' + id).html(data['c_num'])
            }
            if (data['c_num'] == 0){
                $('#cartid' + id).remove()
            }
        },
        error:function(data){
            alert('error')
    }
    })

}

<!-- 页面一刷新，就把购物车的数据展示出来-->

$.get('/axf/shownum/',function(data){
    var carts = data['carts_list']
    if (data['code'] == '200'){
        for(var i=0;i < carts.length;i+=1){

            $('#good_' + carts[i].good_id).html(carts[i].c_num)
        }
    }
})

//算出选中商品的总价

$.get('/axf/totalPrice/',function(data){
  
    $('#total_price').html('总价:'+ data.total)
})

//全选商品
 function FutureGenerations() {
    var value = $('#cart_choice_id').text()
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
     $.ajax({
         url:'/axf/FutureGenerations/',
         type:'POST',
         dataType:'json',
         data:{'value':value},
         headers:{'X-CSRFToken':csrf},
         success:function(data){
             var cart_good_id_list = data['cart_good_id_list']
             for(var i=0;i<cart_good_id_list.length;i+=1){
                 if (cart_good_id_list[i]['is_select']){
                     $('#cart_goods'+ cart_good_id_list[i].cart_id ).html('√')
                      $('#cart_choice_id').html('√')

                 }
                 else{
                      $('#cart_goods'+ cart_good_id_list[i].cart_id ).html('X')
                     $('#cart_choice_id').html('X')
                 }

             }
         },
         error:function(data){
             alert('error')

         }
     })


 }

// 下单
function orderInfo(){
      var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url:'/axf/orderInfo/',
        type:'POST',
        dataType:'json',
        headers:{'X-CSRFToken':csrf},
        success:function(data){
            if(data['code'] == '200'){
                location.href = '/axf/orderInfo/?order_id='+ data['order_id']
            }
        },
        error:function(data){
            alert('请求失败')
        }
    })

}


























