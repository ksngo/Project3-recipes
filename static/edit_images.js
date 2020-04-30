
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
                        data-tabs="file camera facebook instagram dropbox gdrive"
                        data-max-size="1048576"
                        />
    
    `

    document.getElementById("image-id").appendChild(imageElement)

    // --------------------------from uploadcare to limit file size-----------------------------------//
    //------------------ https://uploadcare.com/docs/file_uploads/widget/v2/validation/------//
    function fileSizeLimit(min, max) {
        return function(fileInfo) {
            if (fileInfo.size === null) {
            return
            }
            if (min && fileInfo.size < min) {
            throw new Error('fileMinimalSize')
            }
            if (max && fileInfo.size > max) {
            throw new Error('fileMaximumSize')
            }
        }
        }

    $(function() {
        $('[role=uploadcare-uploader]').each(function() {
            var input = $(this)

            if (!input.data('minSize') && !input.data('maxSize')) {
            return }
            var widget = uploadcare.Widget(input)

        widget.validators.push(fileSizeLimit(input.data('minSize'), input.data('maxSize')))
        })
    })

    // --------------------------end of from uploadcare to limit file size-----------------------------------//
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




