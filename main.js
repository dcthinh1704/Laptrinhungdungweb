const signInBtnLink = document.querySelector('.signInBtn-link')
const signUpBtnLink = document.querySelector('.signUpBtn-link')
const wrapper = document.querySelector(".wrapper")

signUpBtnLink.addEventListener('click', () => {
    wrapper.classList.toggle('active')
})

signInBtnLink.addEventListener('click', () => {
    wrapper.classList.toggle('active')
})

const eye_icon_signup = document.querySelector('.eye-icon-signup')
const password_signup = document.querySelector('.password-signup')

eye_icon_signup.onclick = function () {
    if (password_signup.type == 'password') {
        password_signup.type = 'text'
        eye_icon_signup.classList.remove('fa-eye')
        eye_icon_signup.classList.add('fa-eye-low-vision')
    }
    else {
        password_signup.type = 'password'
        eye_icon_signup.classList.remove('fa-eye-low-vision')
        eye_icon_signup.classList.add('fa-eye')
    }
}

const eye_icon_signin = document.querySelector('.eye-icon-signin')
const password_signin = document.querySelector('.password-signin')
eye_icon_signin.onclick = function () {
    if (password_signin.type == 'password') {
        password_signin.type = 'text'
        eye_icon_signin.classList.remove('fa-eye')
        eye_icon_signin.classList.add('fa-eye-low-vision')
    }
    else {
        password_signin.type = 'password'
        eye_icon_signin.classList.remove('fa-eye-low-vision')
        eye_icon_signin.classList.add('fa-eye')
    }
}