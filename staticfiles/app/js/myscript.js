$('.plus-curt').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    console.log("pid = ",id); // debugging purpose
    $.ajax({
        type:"GET",
        url:'/plusCurt',
        data:{
            prod_id:id
            
        },
        success:function(data){
            console.log("data = ",data); // debugging purpose
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
  
})


$('.minus-curt').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    console.log("pid = ",id); // debugging purpose
    $.ajax({
        type:"GET",
        url:'/minusCurt',
        data:{
            prod_id:id
            
        },
        success:function(data){
            console.log("data = ",data); // debugging purpose
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
  
})

$('.remove-curt').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this
    console.log("pid = ",id); // debugging purpose
    $.ajax({
        type:"GET",
        url:'/removeCurt',
        data:{
            prod_id:id     
        },
        success:function(data){
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
  
})
