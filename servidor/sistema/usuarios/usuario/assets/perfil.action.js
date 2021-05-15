var elem_password = document.getElementById('password_profile')
var new_password = document.getElementById('newpass_profile')
var rep_password = document.getElementById('repeat_profile')

$('#current-eye').on('click', function () {
    if ($(this).html() === 'visibility') {
        $(elem_password).attr('type', 'text')
        $(this).html('visibility_off')
    } else {
        $(elem_password).attr('type', 'password')
        $(this).html('visibility')
    }
});

$('#new-eye').on('click', function () {
    if ($(this).html() === 'visibility') {
        $(new_password).attr('type', 'text')
        $(this).html('visibility_off')
    } else {
        $(new_password).attr('type', 'password')
        $(this).html('visibility')
    }
});

$('#rep-eye').on('click', function () {
    if ($(this).html() === 'visibility') {
        $(rep_password).attr('type', 'text')
        $(this).html('visibility_off')
    } else {
        $(rep_password).attr('type', 'password')
        $(this).html('visibility')
    }
});

validationKeyup("form-data")
validationKeyup("form-credential")

$('#mod-perfil').on('click', function () {
    var notvalid = validationInputSelectsWithReturn("form-data");

    if (!notvalid) {
        objeto = JSON.stringify({
            'id': $('#idpersona').val(),
            'nombre': $('#nombre_profile').val(),
            'apellido': $('#apellido_profile').val(),
            'ci': $('#ci_profile').val(),
            'email': $('#email_profile').val(),
            'telefono': $('#telefono_profile').val(),
            'user': $('#id').val()
        })
        console.log(JSON.parse(objeto))

        $.ajax({
            url: "/usuario_update_profile",
            type: "post",
            data: {object: objeto, _xsrf: getCookie("_xsrf")},
            success: function (response) {
                valor = JSON.parse(response)

                if (valor.success) {
                    show_toast('success', 'Se modificó el perfil de usuario correctamente.')
                    setTimeout(function () { location.reload() }, 2000)
                }
                else show_toast('error', 'No se modificó el perfil de usuario.')
            },
            error: function (jqXHR, status, err) {
                show_toast('warning', jqXHR.responseText);
            }
        });
    }
    else show_toast('warning', 'Por favor, complete todos los campos requeridos (*).')
});

$('#upd-credential').on('click', function () {
    var notvalid = validationInputSelectsWithReturn("form-credential");
    console.log(notvalid)

    if (!notvalid) {
        newp = $('#newpass_profile').val()
        newp1 = $('#repeat_profile').val()

        objeto = JSON.stringify({
            'id': $('#id').val(),
            'username': $('#username_profile').val(),
            'old_password': $('#password_profile').val(),
            'new_password': newp,
            'new_rpassword': newp1
        })

        if (newp === newp1) {
            $.ajax({
                url: "/usuario_update_credential",
                type: "post",
                data: {object: objeto, _xsrf: getCookie("_xsrf")},
            }).done(function (response) {
                valor = JSON.parse(response)

                if (valor.success) {
                    show_toast('success', 'Se modificó las credenciales correctamente.')
                    setTimeout(function () { location.reload() }, 2000)
                }
                else show_toast('error', 'Contraseña actual errónea.')
            })
        } else show_toast('warning', 'Las contraseñas no coinciden.')
    }
    else show_toast('warning', 'Por favor, complete todos los campos requeridos (*).')
});
