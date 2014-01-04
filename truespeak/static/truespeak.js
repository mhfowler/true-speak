$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});





$(document).ready(function()
{

//    function csrfSafeMethod(method) {
//        // these HTTP methods do not require CSRF protection
//        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
//    }
//    $.ajaxSetup({
//        crossDomain: false, // obviates need for sameOrigin test
//        beforeSend: function(xhr, settings) {
//            if (!csrfSafeMethod(settings.type)) {
//                xhr.setRequestHeader("X-CSRFToken", csrftoken);
//            }
//        }
//    });

    /* javascript for /settings/ page */
    var settings_url = "/settings/";

    $(".new_email_save").click(function(e) {
        e.preventDefault();
        $(".settings_success").hide();
        $(".settings_error").hide();
        $(".loading-gif").show();
        var new_email_input = $(".new_email");
        var new_email = new_email_input.val();
        var post_data = {"new_email":new_email};
        $.post(settings_url, post_data, function(data) {
            $(".loading-gif").hide();
            var error = data['error'];
            var message = data['message'];
            if (error == null) {
                $(".settings_success").html(message);
                $(".settings_success").fadeIn();
            }
            else {
                $(".settings_error").html(error);
                $(".settings_error").fadeIn();
            }
        });
    });

    /* javascript for /register/ page */

    var email_input = $(".register_email");
    if (window.location.pathname == "/register/") {
        email_input.focus();
    }

    $(".register_button").click(function(e) {
        e.preventDefault();
        var form_wrapper = $(".register_form");
        var error_div = $(".register_error");
        var loading_gif = $(".loading-gif");
        error_div.hide();
        loading_gif.fadeIn();
        setTimeout(function(){
            var password_input1 = $(".register_password1");
            var password_input2 = $(".register_password2");
            var password1 = password_input1.val();
            var password2 = password_input2.val();
            var email_input = $(".register_email");
            var email_val = email_input.val();
            var post_data = {
                "email":email_val,
                "password1":password1,
                "password2":password2
            };
            $.post("/register/", post_data, function(data) {
                loading_gif.hide();
                var error = data['error'];
                var message = data['message'];
                if (error == '') {
                    // show sound of music image
                    // generate public and private key
                    // password encrypt private key, and store that in local storage too
                    window.location.href = "/welcome/" + email_val + "/";
                    // after confirmation email
                    // upload public key
                    // upload encrypted version of private key
                    // redirect to gmail
                }
                else {
                    error_div.show();
                    error_div.html(error);
                }
            });
        },1000);

    });


    /* javascript for /login/ page */
    var login_email_input = $(".login_email");
    if (window.location.pathname == "/login/") {
        login_email_input.focus();
    }

    $(".login_button").click(function(e) {
        e.preventDefault();
        var error_div = $(".login_error");
        var loading_gif = $(".loading-gif");
        error_div.hide();
        loading_gif.fadeIn();
        var password_input = $(".login_password");
        var password = password_input.val();
        var login_email_input = $(".login_email");
        var email_val = login_email_input.val();
        var post_data = {
            "email":email_val,
            "password":password
        };
        $.post("/login/", post_data, function(data) {
            loading_gif.hide();
            var error = data['error'];
            var message = data['message'];
            if (error == '') {
                //redirect to page they were previously at
                window.location.href = "/settings/"
            }
            else {
                error_div.show();
                error_div.html(error);
            }
        });




    });


});