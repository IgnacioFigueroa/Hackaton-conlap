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
    var chat_body = $('#chat-box');
    $.ajax({
        async: true,
        type : 'GET',
        url: '/get_messages/',
        datatype : 'json',
        success : function (data) {
            for (var i = 0; i < data.length; i++) {
                var message_id = data[i]['message_id'];
                var user_id = data[i]['user_id'];
                var user_name = data[i]['user_name'] + ' ' + data[i]['user_last'];
                var date = data[i]['message_date'];
                var text = data[i]['text'];
                var emotions_sum = data[i]['emotions_sum'];

                chat_body.append($('<div class="' + emotions_sum + '" id="' + message_id + '">').text(text));


            }

        }
    })
}

function removeIrrelevant() {
    if(x === 1){
        $('.I').css('color','white');
        x = 0 ;
        $('#btn-remove-irrelevant').text('Show Irrelevant');
    }
    else{
        $('.I').css('color','black');
        x = 1 ;
        $('#btn-remove-irrelevant').text('Remove Irrelevant');
    }



}

function drawEmotionsChart(data){

}
var x = 1;
$(document).ready(function () {
    getMessages();

    $('#btn-remove-irrelevant').click(removeIrrelevant);
});