
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

    counter++
    counter = counter % bgImageArray.length 
    console.log(counter)

    document.querySelector('body').style.backgroundImage = bgImageArray[counter]
}

setInterval(switchImage, 5000)