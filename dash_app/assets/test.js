let titleEls = document.getElementsByClassName("three_columns")[0];
let btn = document.getElementById("fix");
btn.addEventListener("click",function(){
    titleEls.classList.toggle("hover")
})