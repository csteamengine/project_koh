/**
 * Created by Charlie on 9/8/16.
 */

function cancel_snapshot(){
    $('#result_image').remove();
    returnToWebcam(false);
}

function changeImg(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#upload_img').attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}
function handle_identify_button_pressed(){
    var string = $('#result_image').attr('src') + ",webcamPhoto.jpg" ;
    var image_ws = new WebSocket("ws://localhost:8888/websocket_image?Id=123456789");
    image_ws.onopen = function(){
        image_ws.send(string);
    };
    image_ws.onmessage = function(evt){
        handle_prediction_results_from_server(evt.data);
        image_ws.close();
    };
}

function handle_upload_form_submitted() {
    var input = $('#upload_img').attr('src') + ",webcamPhoto.jpg";
    var image_ws_upload = new WebSocket("ws://localhost:8888/websocket_image?Id=123456789");
    image_ws_upload.onopen = function () {
        image_ws_upload.send(input);
    };
    image_ws_upload.onmessage = function(evt){
        handle_prediction_results_from_server(evt.data);
        image_ws_upload.close();
    };

}

function handle_prediction_results_from_server(data){
    // data format:
    //     encoded_image_string, positive_id, first + "_" + last, student_id, error_string
    var split_data = data.split(',');
    var img = trim_base64(split_data[0]);
    var bool = split_data[1];
    var name = split_data[2].split('_');
    var student_id = split_data[3];
    var error_message = split_data[4];

    if (error_message == "ERROR_NO_FACES_DETECTED") {
        returnToWebcam(true);
    } else if (bool == "True") {
        $('#webcam_div').hide();
        $('#result').show();
        var f_name = name[0];
        var l_name = name[1];
        $('#student_display').attr('src', img);
        $('#first_name').html(f_name.toString());
        $('#last_name').html(l_name.toString());
    }else{
        display_student_identification_modal(student_id, img);
    }
}

function wrong_student_identified() {
    var img = $("#snapshot_result").data;
    var id = $("#id").val;

    display_student_identification_modal(id, img);
}

function trim_base64(data){
    var img = data;
    img = img.replace('\'', '');
    img = img.substr(0,img.length -1);
    img = img.substr(1);
    img =  'data:image/jpeg;base64,' + img;
    return img;
}

function display_student_identification_modal(student_id, encoded_img){
    // When the user clicks on the button, open the modal
    $('#myModal').show();
    $('#id').val(student_id);
    // var img = trim_base64(encoded_img);
    // $('#modal_image').attr('src', img);
    $('#modal_image').attr('src', encoded_img);
}

function take_snapshot() {
    Webcam.snap(function (data_uri) {
        document.getElementById('snapshot_result').innerHTML = '<img id="result_image" src="' + data_uri + '"/>';
    });
}

function send_newstudent(first, last, id) {
    var ws_newstudent = new WebSocket("ws://localhost:8888/websocket_newstudent");
    ws_newstudent.onopen = function () {
        //Do Something
        ws_newstudent.send(first + "," + last + "," + id);
    };
    ws_newstudent.onmessage = function (evt) {
        console.log(evt.data);
        if (evt.data === "SUCCESS") {
            $("#myModal").hide();
        }
        ws_newstudent.close();
    };

    var string = $('#modal_image').attr('src') + ",webcamPhoto.jpg" ;
    var image_ws = new WebSocket("ws://localhost:8888/websocket_image?Id=123456789");
    image_ws.onopen = function(){
        image_ws.send(string);
    };
    image_ws.onmessage = function(evt){
        handle_prediction_results_from_server(evt.data);
        image_ws.close();
    };
}