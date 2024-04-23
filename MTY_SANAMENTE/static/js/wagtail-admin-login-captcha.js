function onRecaptchaVerify(response) {
    $('#wagtail-login-captcha-button').removeClass('disabled')
    setTimeout(() => {
        $('#wagtail-login-captcha-button').addClass('disabled')
    }, 60000);
}

$(document).on("keydown", "form", function (event) {
    const classes = $('#wagtail-login-captcha-button').attr("class");
    return classes.includes('disabled') ? event.key !== "Enter" : true;
});