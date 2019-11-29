window.onload = updateData;

function updateData() {
    var timeout = 5000;
    getData();
    setTimeout(updateData, timeout);
}

function getData(){
    url = "http://localhost:8055/ui/ajax/dashboard_update/";
    $.post(
        url,
        {
            ajaxUserToken: $('#ajaxUserToken').val(),
            csrfmiddlewaretoken: $('#ajaxCsrfToken').val()
        },
        function(data){
            // alert("got a response: " + data.total_msgs + "\nStatus: " + status)
            $("#ajaxTotalSent").text(data.total_msgs);
        },
        "json");
    var today = new Date();
    var date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
    var time = today.getHours() + ':' + today.getMinutes() + ':' + today.getSeconds();
    var dateTime = date + ' ' + time;
    $(ajaxLastUpdate).text(dateTime);
}