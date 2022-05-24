const date_search_input = document.getElementById("date-search-input");
const submit_btn = document.getElementById("submit-form");

date_search_input.addEventListener("change", function(){
    console.log(date_search_input.value,"new value is");
    submit_btn.submit();
});


const date_search_input_low_range = document.getElementById("date-search-input_low_range");
const date_search_input_heigh_range = document.getElementById("date-search-input_heigh_range");