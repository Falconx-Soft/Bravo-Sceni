const event_quantity = document.querySelectorAll("#event-quantity");
let product_id = "";
let product_quantity = "";
let event_id = "";
const p_quantities = document.getElementById("p-quantities");
const p_ids = document.getElementById("p-ids");

for(let i=0; i<event_quantity.length; i++){
    if(event_quantity[i] !=""){
        product_id += event_quantity[i].getAttribute("data-step")+",";
        event_id += event_quantity[i].getAttribute("data-evntID")+",";
        product_quantity += event_quantity[i].value+",";
    }
}

document.getElementById("event-ids").value = event_id
p_quantities.value = product_quantity;
p_ids.value = product_id;

for(let i=0; i<event_quantity.length; i++){
    event_quantity[i].addEventListener("change", function(){
        if (product_id.indexOf(event_quantity[i].getAttribute("data-step")) > -1){
            console.log("already exist");
            let temp_id = product_id.split(",");
            let temp_product_quantity = product_quantity.split(",");
            for(let x=0; x<temp_id.length; x++){
                if(temp_id[x]==event_quantity[i].getAttribute("data-step")){
                    temp_product_quantity[x]= event_quantity[i].value;
                }
            }
            product_quantity = "";
            for(let x=0; x<temp_product_quantity.length-1; x++){
                product_quantity += temp_product_quantity[x]+",";
            }
        }else{
            product_id += event_quantity[i].getAttribute("data-step")+",";
            product_quantity += event_quantity[i].value+",";
        }
        
        p_quantities.value = product_quantity;
        p_ids.value = product_id;
    });
}