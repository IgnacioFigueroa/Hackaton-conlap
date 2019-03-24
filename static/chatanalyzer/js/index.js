function getchart(){
    $.ajax({
        async: true,
        type:'GET',
        url : '/get_chart_data/',
        dataType : 'json',
        success: function(data){
            drawEmotionsChart(data);
        },
        error: function () {
            console.log("i got an error")
        }
    })
}

function getMessages() {
    $.ajax({
        async: true,
        type : 'GET',
        url: '/get_messages/',
        datatype : 'json',
        success : function (data) {

        }
    })
}

function drawEmotionsChart(data){

}

$(document).ready(function () {
    getchart()
});