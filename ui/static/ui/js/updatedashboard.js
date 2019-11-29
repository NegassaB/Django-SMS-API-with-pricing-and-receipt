window.onload = updateData;

function updateData(){
    $("#ajaxTotalSent").text("changed by jquery");
    url = "http://localhost:8055/ui/ajax/dashboard_update/";
    $.post(
        url,
        {ajaxUserToken: $('#ajaxUserToken').val()},
        function(){
            alert("got a response")
        });
}