$("#logout_button").click(function(){
    url = "http://localhost:8055/ui/logout_request/"
    $.get(
        url,
        function(data){
            window.location.href = url;
        },
    );
});