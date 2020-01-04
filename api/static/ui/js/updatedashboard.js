window.onload = updateData;

function updateData() {
    var timeout = 10000;
    getData();
    setTimeout(updateData, timeout);
}

function getData(){
    url = "http://localhost:8055/ui/dashboard_update/";
    $.post(
        url,
        {
            ajaxUserToken: $('#ajaxUserToken').val(),
            csrfmiddlewaretoken: $('#ajaxCsrfToken').val()
        },
        function(data){
            if (data.total_msgs != 0 || data.total_msgs != null) {
                // alert("got a response: " + data.total_msgs + "\nStatus: " + status)
                $("#ajaxTotalSent").text(data.total_msgs);
            }
            if(data.last5_sent !=0 || data.last5_sent != null) {
                $("#ajaxLast5minSent").text(data.last5_sent)
            }
            if(data.last5_sent == null){
                $("#ajaxLast%minSent").text(0)
            }
        },
        "json");
    var today = new Date();
    var date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
    var time = today.getHours() + ':' + today.getMinutes() + ':' + today.getSeconds();
    var dateTime = date + ' ' + time;
    $(ajaxLastUpdate).text(dateTime);
}