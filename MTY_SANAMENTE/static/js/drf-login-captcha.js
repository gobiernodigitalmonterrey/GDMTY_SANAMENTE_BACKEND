function onRecaptchaVerify(response) {
    const loginButton = document.getElementById('submit-id-submit')
    loginButton.removeAttribute('disabled')
    setTimeout(() => {
        loginButton.setAttribute('disabled', 'disabled')
    }, 60000);
}

document.addEventListener("keydown", function(event) {
    console.log("event.target.tagName", event.target.tagName)
    if (event.target.tagName === "INPUT") {
        const loginButton = document.getElementById('submit-id-submit');
        if (loginButton && loginButton.hasAttribute('disabled') && event.key === "Enter") {
            event.preventDefault(); // Previene el comportamiento predeterminado del Enter
        }
    }
});