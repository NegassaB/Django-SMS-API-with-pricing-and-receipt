$("#logout_button").click(function(){
    url = "http://localhost:8055/ui/logout_request/"
    $.get(
        url,
        function(data){
            window.location.href = url;
        },
    );
}); 

// $("#logout_button").click(
//     function() {
//         $.get(
//             "http://localhost:8055/ui/logout/",
//             function(data) {
//                 window.alert(data);
//                 window.location.href.replace(data.redirect_url);
//             }
//         );
//         }
// );

// function getData(){
//     url = "http://localhost:8055/ui/ajax/dashboard_update/";
//     $.post(
//         url,
//         {
//             ajaxUserToken: $('#ajaxUserToken').val(),
//             csrfmiddlewaretoken: $('#ajaxCsrfToken').val()
//         },
//         function(data){
//             if (data.total_msgs != 0 || data.total_msgs != null) {
//                 // alert("got a response: " + data.total_msgs + "\nStatus: " + status)
//                 $("#ajaxTotalSent").text(data.total_msgs);
//             }
//             if(data.last5_sent !=0 || data.last5_sent != null) {
//                 $("#ajaxLast5minSent").text(data.last5_sent)
//             }
//         },
//         "json");