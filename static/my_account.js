
$(function(){

document.getElementById('password').addEventListener('keyup',checkPassword)
document.getElementById('password-rekey').addEventListener('keyup',checkPassword)
// document.getElementById('edit-account').addEventListener('click', editAccount)
document.getElementById("user-name").addEventListener("keyup", readySubmitButton)
document.getElementById("password").addEventListener("keyup", readySubmitButton)
document.getElementById("password-rekey").addEventListener("keyup", readySubmitButton)
document.getElementById("email").addEventListener("keyup", readySubmitButton)
document.getElementById("country").addEventListener("keyup", readySubmitButton)

if (document.getElementById("password").value != "" ) {
    
    checkPassword()
}


})


function checkPassword() {

    password = document.getElementById('password').value
    passwordRekey = document.getElementById('password-rekey').value


    if (document.getElementById("password").value == "" ) {

        document.getElementById('pw-span').innerHTML = "&emsp; Password missing."
        document.getElementById('pw-span').style.color ='red'

    } else if (password == passwordRekey) {

        document.getElementById('pw-span').innerHTML = "&emsp; Password matches"
        document.getElementById('pw-span').style.color ='green'

    }  else {

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


function readySubmitButton () {

    console.log("in function")
    document.getElementById("acc-submit").disabled = true
    document.getElementById("acc-submit").style.cursor = "default"

    if (document.getElementById("user-name").value != "" ) {
        console.log(1)
        if(document.getElementById("password").value != "") {
            console.log(2)
            if(document.getElementById("pw-span").innerHTML == "  Password matches") {
                console.log(3)
                if(document.getElementById("email").value != "" ) {
                    console.log(4)
                    if(document.getElementById("country").value != "") {

                        document.getElementById("acc-submit").disabled = false
                        document.getElementById("acc-submit").style.cursor = "pointer"
                    } 
                }
            }
        }
    } 
} 