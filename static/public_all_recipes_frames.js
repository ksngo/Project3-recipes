
$(function(){

    let element  = document.getElementsByClassName("recipe-name-link")
    
    for (let i of element) {
        i.addEventListener("mouseover", turn_dark)
        i.addEventListener("mouseout", turn_light)
    }

})

function turn_dark(){

    this.style.backgroundColor = "rgba(255,99,71,1)"


}

function turn_light(){
    this.style.backgroundColor = "rgba(255,99,71,.8)"
}