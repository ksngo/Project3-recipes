
$(function(){

    document.getElementById("bookmark").addEventListener("click" , bookmarkDialog)
    document.getElementById("close-dialog").addEventListener("click", closeDialog)


})

function bookmarkDialog () {

    document.getElementById("bookmark-dialog").style.display = "block"
    document.getElementsByTagName("body")[0].style.backgroundColor = "rgba(169,169,169,.2)"
    

    let numberAnchorTags = document.getElementsByTagName("a").length

    for (i=0 ; i <numberAnchorTags ; i++) {
        document.getElementsByTagName("a")[i].classList.add ("inactiveLink")
    }

    document.getElementById("button-ratings").classList.add ("inactiveLink")

}

function closeDialog () {

    document.getElementById("bookmark-dialog").style.display="none"
    document.getElementsByTagName("body")[0].style.backgroundColor = "rgba(255,255,255,0)"

    let numberAnchorTags = document.getElementsByTagName("a").length

    for (i=0 ; i <numberAnchorTags ; i++) {
        document.getElementsByTagName("a")[i].classList.remove ("inactiveLink")
    }

    document.getElementById("button-ratings").classList.remove ("inactiveLink")

}