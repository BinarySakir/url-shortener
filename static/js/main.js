$(function() {
    $("form").submit(function (e) {
        e.preventDefault();
        var originalUrl = $('.form-control').val();
        $.ajax({
            url: '/urlShortener',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                var data = jQuery.parseJSON(response);
                if(data.status == 'OK'){
                    $('form').nextAll().remove();
                    var shortUrl = "http://127.0.0.1:5000/" + data.message;
                    $(".col-md-6").append(
                        "<input type='text' class='copyurl' value='" + shortUrl + "' readonly='readonly'>"+
                        "<p>Press Ctrl+C to Copy</p>"
                        ).fadeIn('slow');
                    $("input[type='text']").focus().select();
                }else{
                    $('form').nextAll().remove();
                    $(".col-md-6").append("<div class='error'>" + data.message + "</div>").fadeIn('slow');
                }
            },
            error: function(error) {
                alert("Something Went Wrong!");
            }
        });
    });
});
