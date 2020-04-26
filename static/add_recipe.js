
$(function(){

document.getElementById('add-row').addEventListener('click',addRow)


})

function addRow() {

    console.log('success in addrow')
    let rowElement = document.createElement('div')
    rowElement.innerHTML = `
        <input type='text' name='step1' placeholder='insert step'/>`
    
    document.getElementById('add-recipe').appendChild(rowElement)

}




