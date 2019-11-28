window.onload = updateData;

function updateData(){
    document.getElementById("ajaxTotalSent").innerHTML = "changed";
    document.getElementById("ajaxLast5minSent").innerHTML = "this also changed";
    document.getElementById("ajaxLastUpdate").innerHTML = "last but not least, changed as well";
}