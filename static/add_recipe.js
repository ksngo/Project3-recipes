$(function () {
  document.getElementById("add-step-np").addEventListener("click", addStep);

  document.getElementById("minus-step-np").addEventListener("click", minusStep);

  document.getElementById("add-image-np").addEventListener("click", addImage);

  document
    .getElementById("minus-image-np")
    .addEventListener("click", minusImage);
});

function addStep() {
  NumExistingSteps = document.getElementById("steps-rows").childElementCount;

  // **************to count the number of steps at present****************//
  document.getElementById("num-steps-np").value = NumExistingSteps + 1;

  let stepElement = document.createElement("div");

  // stepElement.setAttribute("class","form-group row")
  stepElement.innerHTML = `
                <div class="form-group row">
                    <label class="col-sm-2 col-form-label"> <b>STEP ${
                      NumExistingSteps + 1
                    }</b> </label>
                    <div class="col-sm-10">
                        <input class="form-control" type="text" name="step-${NumExistingSteps}" value="" />
                    </div>
                </div>
                <div class="form-group row">
                    <label class="col-sm-2 col-form-label"> Ingredients for Step ${
                      NumExistingSteps + 1
                    } </label>
                    <div class="col-sm-10">
                        <input class="form-control" type="text" name="ing-${NumExistingSteps}" value="" />
                    </div>
                </div>
                <div class="form-group row">
                    <label class="col-sm-2 col-form-label"> Tools for step ${
                      NumExistingSteps + 1
                    }  </label>
                    <div class="col-sm-10">
                        <input class="form-control" type="text" name="tools-${NumExistingSteps}" value="" />
                    </div>
                </div>`;

  document.getElementById("steps-rows").appendChild(stepElement);
}

function minusStep() {
  if (document.getElementById("steps-rows").childElementCount == 1) {
    alert("Step 1 is shown by default.");
  } else if (
    confirm(
      "All contents in last step will be erased. Continue to remove last step?"
    )
  ) {
    document.getElementById("steps-rows").lastElementChild.remove();

    NumExistingSteps = document.getElementById("steps-rows").childElementCount;

    // **************to count the number of steps at present****************//
    document.getElementById("num-steps-np").value = NumExistingSteps;
  }
}

function addImage() {
  NumOfSpan = document.getElementById("image-id").childElementCount;

  NumImages = NumOfSpan + 1;
  console.log(NumImages);
  document.getElementById("num-images-np").value = NumImages;

  imageElement = document.createElement("span");

  imageElement.classList.add("uploader-button");
  imageElement.innerHTML = `
    
                <input 
                        type="hidden"
                        role="uploadcare-uploader"
                        name="image-${NumOfSpan}"
                        data-tabs="file camera facebook instagram dropbox gdrive"
                        data-max-size="1048576" />
    
    `;

  document.getElementById("image-id").appendChild(imageElement);

  // --------------------------from uploadcare to limit file size-----------------------------------//
  //------------------ https://uploadcare.com/docs/file_uploads/widget/v2/validation/ ------//

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
      return
    }
    var widget = uploadcare.Widget(input)

    widget.validators.push(fileSizeLimit(input.data('minSize'), input.data('maxSize')))
  })
})
// --------------------------End of from uploadcare to limit file size-----------------------------------//
  
}

function minusImage() {
  NumOfSpan = document.getElementById("image-id").childElementCount;

  if (NumOfSpan > 1) {
    document.getElementById("image-id").lastElementChild.remove();
    document.getElementById("num-images-np").value = NumOfSpan - 1;
  } else {
    alert(" An Image Upload button shown by default.");
  }
}
