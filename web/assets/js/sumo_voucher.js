$(function() {
    var $alert_box = $('#confirm-voucher-alert-box');
    var $scan_qr_button = $('#scan-qr-button');
    var $scan_qr_camera_input = $('#scan-qr-camera-input');

    var $code_input = $('#voucher-code');
    var $submit_confirm_voucher = $('#submit-confirm-voucher');    

    var confirm_voucher = function(url) {
        $alert_box.hide();
        $.ajax({
            url: url,
            type: 'POST',
            success: function(d) {
                render_alert($alert_box, d, 'alert-success');
            },
            error: function(e) {
                render_alert($alert_box, e.responseText, 'alert-danger'); 
            }
        })
    }

    var confirm_voucher_by_code = function(code) {
        var url = '/confirm-voucher?code=' + code;
        confirm_voucher(url);
    }

    function scan_qr_callback(result) {
        $alert_box.hide();
        if ( result.startsWith('error') ) {
            render_alert($alert_box, 'Error scanning QR Code, please retake the picture or type in voucher code', 'alert-danger');
            return false;
        }
        confirm_voucher(result);
    }

    $scan_qr_camera_input.on('change', function() {
        if ( this.files.length <= 0 ) { return false; }
        var file = this.files[0];
        var reader = new FileReader();
        reader.onload = (function(f) {
            return function(e) {
                qrcode.decode(e.target.result);
            }
        })(file);
        reader.readAsDataURL(file);        
    });    

    $submit_confirm_voucher.on('click', function() {
        $alert_box.hide();
        var code = $code_input.val().replace(/ /g,'');
        if (code === '') { 
            render_alert($alert_box, 'Please enter a valid voucher code', 'alert-danger'); 
            return false;
        };
        confirm_voucher_by_code(code);
    });

    qrcode.callback = scan_qr_callback;
});
