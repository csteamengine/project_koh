/**
 * Created by Charlie on 9/8/16.
 */

function cancel_snapshot(){
    $('#result_image').remove();
    $('#webcam_identify').hide();
    $('#cancel_webcam').hide();
    $('#upload_button').show();
    $('#my_camera').show();
    $('#take_snapshot_button').show();
    $('#my_result').hide();
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
function send_webcam_photo(){
    var string = $('#result_image').attr('src') + ",webcamPhoto.jpg" ;
    var image_ws = new WebSocket("ws://localhost:8888/websocket_image?Id=123456789");
    image_ws.onopen = function(){
        image_ws.send(string);
    };
    image_ws.onmessage = function(evt){
        display_student(evt.data);
    };
}

function readURL() {
    var input = $('#upload_img').attr('src') + ",webcamPhoto.jpg";
    var image_ws_upload = new WebSocket("ws://localhost:8888/websocket_image?Id=123456789");
    image_ws_upload.onopen = function () {
        image_ws_upload.send(input);
    };
    image_ws_upload.onmessage = function(evt){
        display_student(evt.data);
    };

}

function display_student(data){
    $('#result').show();
    var data = data.split(',');
    var img = trim_base64(data[0]);
    var name = data[1].split('_');

    if(name != null){
        var f_name = name[0];
        var l_name = name[1];
        $('#student_display').attr('src', img);
        $('#first_name').html(f_name.toString());
        $('#last_name').html(l_name.toString());
    }else{
        send_new_student(data);
    }

}

function trim_base64(data){

    var img = data;
    img = img.replace('\'', '');
    img = img.substr(0,img.length -1);
    img = img.substr(1);
    img =  'data:image/jpeg;base64,' + img;
    return img;

}
