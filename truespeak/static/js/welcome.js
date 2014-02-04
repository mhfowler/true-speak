$(document).ready(function() {
    var timeout = 5;

    setInterval(function() {
        $(".loading-time").text(timeout);
        timeout--;
    }, 1000);
    
    setTimeout(function() {
        window.location.replace("https://mail.google.com");
    }, timeout * 1000);

});