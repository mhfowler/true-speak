function flashMessage($elm, message, flashMessageDelay) {
    // flash message after this many ms
    var flashMessageDelay = flashMessageDelay || 1500;
    //cancel old animations
    $elm.dequeue();
    $elm.html(message);
    $elm.fadeIn().delay(flashMessageDelay).fadeOut('slow');
}

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

$(document).ready(function() {
    /* javascript for /register/ page */

    var email_input = $(".register_email");
    if (window.location.pathname == "/register/") {
        email_input.focus();
    }

    /* javascript for /login/ page */
    var login_email_input = $(".login_email");
    if (window.location.pathname == "/login/") {
        login_email_input.focus();
    }

    setTimeout(function() {
            var anon_function = function() {
                var no_ext = $(".no_ext_installed");
                no_ext.click(function(e) {
                    e.preventDefault();
                    var extension_link = "https://chrome.google.com/webstore/detail/parseltongue/egpagjaeoilneaefepllapmajaoefcgd?hl=en&gl=US";
                    $(".register_error").html("To register for ParselTongue you must first <a href='" + extension_link + "'>install the extension.</a>");
                    $(".register_error").show();
                    $(".login_error").html("To login to ParselTongue you must first <a href='" + extension_link + "'>install the extension.</a>");
                    $(".login_error").show();
                });
            };
            anon_function();
        }, 100
    );



});