$("#logout_button").click(function(){
    url = "http://localhost:8055/ui/logout_request/"
    $.get(
        url,
        function(data){
            if(data == null){
                window.alert("no workings");
            } else {
                window.location.assign(data.redirect_url);
            }
        },
    );
});