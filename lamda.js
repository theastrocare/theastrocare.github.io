// Set 'URL' to your API Gateway endpoint
URL = 'https://jig1qbpypa.execute-api.us-east-1.amazonaws.com/PROD/';

$(document).ready(function () {

    $("#mainForm").submit(function (e) {
        e.preventDefault();
        
        var name = $("#Name").val(),
            City = $("#City").val(),
            DOB = $("#DOB").val(),
            TOB = $("#TOB").val();

        $.ajax({
            type: "POST",
            url: URL,
            contentType: 'application/json',
            crossDomain: true, // remove in production environments
            dataType: 'json',
            dataType: 'jsonp', // use JSONP for done() callback to work locally
            data: JSON.stringify({
                name: name,
                City: City,
                DOB: DOB,
                TOB: TOB

            })
        }).done(function (result) {
            console.log(result);
        }).fail(function (jqXHR, textStatus, error) {
            console.log("Post error: " + error);
            if (error != '') $('#form-response').text('Error: ' + error);
        }).always(function(data) {
            console.log(JSON.stringify(data));
            $('#form-response').text('Your Details have been submitted. Thank You!');
        });

    });
});