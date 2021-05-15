var elem_password = document.getElementById('password')

validationKeyup("sign_in")

function show_alert(ida, message) {
    $('.alert-invalid').remove()
    $('\
        <div class="alert bg-red align-center animated flipInX alert-invalid" style="vertical-align: middle">\
            <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>\
            <i class="material-icons md-18">warning</i> <span class="p-b-15">' + message + '</span>\
        </div>\
    ').insertAfter(ida)
}

$('#btn-login').on('click',function (e) {
    e.preventDefault();
    var notvalid = validationInputSelectsWithReturn("sign_in");

    if (!notvalid) {
        dt_object = JSON.stringify({
            'username': $('#username').val(),
            'password': $('#password').val()
        })
        $('#btn-login').html('\
            <div class="preloader pl-size-xs">\
                <div class="spinner-layer pl-white">\
                    <div class="circle-clipper left">\
                        <div class="circle"></div>\
                    </div>\
                    <div class="circle-clipper right">\
                        <div class="circle"></div>\
                    </div>\
                </div>\
            </div>\
            <span class="vertical-own">Verificando</span>\
        ')

        ajax_call_get('usuario_autenticacion', {
            _xsrf: getCookie("_xsrf"),
            object: dt_object
        }, function (response) {
            var self = response;

            if (self.success) {
                ajax_call_login('/inicio', {
                    _xsrf: getCookie("_xsrf"),
                    object: dt_object
                }, function (response) {
                    if (response.success) {
                        setTimeout(function () {
                            window.location = '/';
                        }, 1000)
                    } else {
                        show_alert('#msg-info', 'Datos de usuario incorrectos.')
                        $('#btn-login').html('INICIAR');
                    }
                });
            } else {
                show_alert('#msg-info', self.message)
                $('#btn-login').html('INICIAR');
            }
        })
    }
    else show_alert('#msg-info', notvalid);
 })

$('#password').keydown(function (e) {
    if (e.keyCode === 13) $('#btn-login').click();
});

$('#cont-eye').on('click', function () {
    if ($(this).html() === 'visibility') {
        $(elem_password).attr('type', 'text')
        $(this).html('visibility_off')
    } else {
        $(elem_password).attr('type', 'password')
        $(this).html('visibility')
    }
});
