console.log('success')
$(function(){

document.getElementById('password-rekey').addEventListener('keyup',checkPassword)

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

