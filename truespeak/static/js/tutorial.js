$(function() {
    var $carousel = $('#tutorial-carousel');

    $('.carousel-image').click(function() {
        $carousel.carousel('next');
    });

});