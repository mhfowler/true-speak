$('.resend-confirmation').tooltip({
    'title' : 'Resend confirmation link',
});

/* javascript for /settings/ page */
var settingsUrl = "/settings/";

$(".new-email-save").click(function(e) {
    e.preventDefault();

    $(".settings-success").hide();
    $(".settings-error").hide();
    $(".loading-gif").show();

    var newEmailInput = $(".new-email");
    var newEmail = newEmailInput.val();
    var postData = {
        "new_email":newEmail, 
    };

    $.post(settingsUrl, postData, function(data) {
        $(".loading-gif").hide();
        var error = data['error'];
        var message = data['message'];

        if (error === null) {

            flashMessage($('.settings-success'), message);

            $emailElm = $('<li class="list-group-item email-address">' +
                    newEmail +
                    '<div class="email-btn delete-email" email="' + newEmail + '">' +
                        '<span class="glyphicon glyphicon-remove"></span>' + 
                    '</div>' + 
                    '<div class="email-btn resend-confirmation">' + 
                        '<span class="glyphicon glyphicon-envelope"></span>' + 
                    '</div>' + 
                '</li>');
            $emailElm.find('.delete-email').click(function() {
                deleteEmailHandler($(this));
            });
            $('.list-group').append($emailElm);
        }
        else {
            flashMessage($('.settings-error'), error);
        }
    });
});

function deleteEmailHandler($elm) {
    var $emailElm = $elm.closest('.email-address');
    var deleteEmail = $elm.attr('email');
    var postData = {
        'delete_email' : deleteEmail,
    }
    $.post(settingsUrl, postData, function(data) {
        if (data['error'] == null) {
            $emailElm.remove();
        }
    });
}

$('.delete-email').click(function() {
    deleteEmailHandler($(this));
});
