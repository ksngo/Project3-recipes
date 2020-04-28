console.log('success')
$(function(){

document.getElementById('password-rekey').addEventListener('keyup',checkPassword)
// document.getElementById('edit-account').addEventListener('click', editAccount)
})


function checkPassword() {

    console.log('hello i am in checkpassword function')
    password = document.getElementById('password').value
    passwordRekey = document.getElementById('password-rekey').value
    if (password == passwordRekey) {

        document.getElementById('pw-span').innerHTML = "&emsp; Password matches"
        document.getElementById('pw-span').style.color ='green'

    } else {

        document.getElementById('pw-span').innerHTML = "&emsp; Password does not match"
        document.getElementById('pw-span').style.color ='red'

    }
}

// function editAccount() {
//     document.getElementById("user-name").readOnly = false
//     document.getElementById("password").readOnly = false
//     document.getElementById("password-rekey").readOnly = false
//     document.getElementById("email").readOnly = false
//     document.getElementById("country").readOnly = false
//     document.getElementById("birthday").readOnly = false
//     document.getElementById("ethnic").readOnly = false
//     document.getElementById("edit-account").style.opacity = "0"
//     // document.getElementById("edit-account").style.color = "lightgrey"
//     document.getElementById("edit-account").style.cursor = "default"
// }

