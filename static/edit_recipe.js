
$(function(){

    document.getElementById("add-step").addEventListener("click", addStep)

    document.getElementById("minus-step").addEventListener("click", minusStep)


})

function addStep() {

    NumExistingSteps = document.getElementById("steps-rows").childElementCount

    // **************to count the number of steps at present****************//
    document.getElementById("num-steps").value = NumExistingSteps + 1

    let stepElement = document.createElement('div')

    // stepElement.setAttribute("class","form-group row")
    stepElement.innerHTML = `
                <div class="form-group row">
                    <label class="col-sm-2 col-form-label"> <b>STEP ${NumExistingSteps+1}</b> </label>
                    <div class="col-sm-10">
                        <input class="form-control" type="text" name="step-${NumExistingSteps}" value="" />
                    </div>
                </div>
                <div class="form-group row">
                    <label class="col-sm-2 col-form-label"> Ingredients for Step ${NumExistingSteps+1} </label>
                    <div class="col-sm-10">
                        <input class="form-control" type="text" name="ing-${NumExistingSteps}" value="" />
                    </div>
                </div>
                <div class="form-group row">
                    <label class="col-sm-2 col-form-label"> Tools for step ${NumExistingSteps+1}  </label>
                    <div class="col-sm-10">
                        <input class="form-control" type="text" name="tools-${NumExistingSteps}" value="" />
                    </div>
                </div>`

    document.getElementById("steps-rows").appendChild(stepElement)


}

function minusStep() {

    if( document.getElementById('steps-rows').childElementCount == 1) {
        alert("Step 1 is shown by default.")
    }else if(confirm('All contents in last step will be erased. Continue to remove last step?')){
        
        document.getElementById('steps-rows').lastElementChild.remove()

        NumExistingSteps = document.getElementById("steps-rows").childElementCount

        // **************to count the number of steps at present****************//
        document.getElementById("num-steps").value = NumExistingSteps
    }
}