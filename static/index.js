
let bgImageArray = []

$(function (){

    bgImageArray = new Array(

        "url(/static/images/retro3.jpg)",
        "url(/static/images/cook2.jpg)",
        "url(/static/images/cook.jpg)",        
        "url(/static/images/chef.png)",
        "url(/static/images/retro.jpg)",
        "url(/static/images/chefs.jpg)",
        "url(/static/images/retro2.jpg)",
        "url(/static/images/cooking.jpg)"

    )
    

    

})

let counter =0

function switchImage () {

    if (document.getElementById("sample-body").style.display == "" || document.getElementById("sample-body").style.display == "none" ) {
    counter++
    counter = counter % bgImageArray.length 
    console.log(counter)

    document.querySelector('body').style.backgroundImage = bgImageArray[counter]

    } 
}

setInterval(switchImage, 5000)


$(function(){

    document.getElementById("show-recipe-sample").addEventListener("click" , showRecipeSample)
    document.getElementsByTagName('span')[0].addEventListener("click" , closeRecipeSample)

})


function showRecipeSample() {   

    document.getElementById("sample-body").style.display = "block"
    document.getElementsByTagName('body')[0].style.backgroundImage = 'url(/static/images/cook2-sepia.jpg)'
    
    
}

function closeRecipeSample() {

    document.getElementById("sample-body").style.display = "none"
    document.getElementsByTagName('body')[0].style.backgroundImage = 'url(/static/images/cook2.jpg)'
    

}