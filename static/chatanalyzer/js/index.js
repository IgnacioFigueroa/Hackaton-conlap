function getchart(){
    $.ajax({
        async: true,
        type:'GET',
        url : '/get_chart_data/',
        dataType : 'json',
        success: function(data){
            console.log(data);
            drawEmotionsChart(data);
        },
        error: function () {
            console.log("i got an error")
        }
    })
}

function drawEmotionsChart(data){

}

$(document).ready(function () {
    getchart()
});