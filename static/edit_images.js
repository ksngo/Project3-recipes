
$(function(){
    
    document.getElementById("add-image-edit-pg").addEventListener("click", addImage)

    document.getElementById("minus-image-edit-pg").addEventListener("click", minusImage)

})


function addImage() {

    NumOfSpan = document.getElementById('image-id').childElementCount

    NumImages = NumOfSpan + 1
    document.getElementById("num-images-edit-pg").value = NumImages
    
    imageElement = document.createElement("span")

    imageElement.classList.add("uploader-button")
    imageElement.innerHTML = `
    
                <input 
                        type="hidden"
                        role="uploadcare-uploader"
                        name="image-${NumOfSpan}"
                        data-tabs="file camera facebook instagram dropbox gdrive" />
    
    `

    document.getElementById("image-id").appendChild(imageElement)

    
}

function minusImage() {

    NumOfSpan = document.getElementById("image-id").childElementCount

    if (NumOfSpan > 1) {
        document.getElementById("image-id").lastElementChild.remove()
        document.getElementById("num-images-edit-pg").value = NumOfSpan - 1
    } else {
        alert(" An Image Upload button shown by default.")
    }
    
}