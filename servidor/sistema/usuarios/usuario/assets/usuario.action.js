var class_item = '.item-form';
var id_table = '#data_table';
var elem_password = '#password';
var fkrol = '#fkrol';

$(document).ready( function () {
    reload_table();
});
validationKeyup("modal")

$('#item-eye').on('click', function () {
    if ($(this).html() === 'visibility') {
        $(elem_password).attr('type', 'text')
        $(this).html('visibility_off')
    } else {
        $(elem_password).attr('type', 'password')
        $(this).html('visibility')
    }
});

$('#fkrol').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar rol',
    title: 'Seleccione un rol'
})

function load_table(data_tb) {
    var tabla = $(id_table).DataTable({
        destroy: true,
        data: data_tb,
        columns: [
            { title: "ID", data: "id", visible: false },
            { title: "Nombre Completo", data: "nombre" },
            { title: "Nombre de Usuario", data: "username" },
            { title: "Foto", data: "foto" },
            { title: "Rol", data: "rol" },
            { title: "Estado", data: "estado",
                render: function(data, type, row) {
                    return '\
                    <div title="' + row.estado + '">\
                        <input id="enabled' + row.id + '" type="checkbox" class="chk-col-indigo enabled" onclick="set_enable(this)" data-id="' + row.id + '" ' + row.check + ' ' + row.disable + '>\
                        <label for="enabled' + row.id + '"></label>\
                    </div>'
                }
            },
            { title: "Acciones", data: "id",
                render: function(data, type, row) {
                    a = ''
                    if (row.disable === '') {
                        a += '\
                            <button data-json="' + data + '"  type="button" class="btn btn-primary waves-effect mr-3-own" title="Editar" onclick="edit_item(this)">\
                                <i class="material-icons">edit</i>\
                            </button>'
                    }
                    if (row.delete) {
                        a += '\
                            <button data-json="' + data + '"  type="button" class="btn btn-danger waves-effect" title="Eliminar" onclick="delete_item(this)">\
                                <i class="material-icons">clear</i>\
                            </button>'
                    }
                    if (a === '') a = 'Sin permisos';
                    return a
                }
            },
        ],
        dom: "Bfrtip",
        buttons: [
            {
                extend: 'excelHtml5',
                className: 'btn btn-sm cb-btn-teal',
                exportOptions: {
                    columns: [ 0, 1, 2, 3 ]
                },
                sheetName: 'Logs',
            },
            {
                extend: 'csvHtml5',
                className: 'btn btn-sm cb-btn-info',
                exportOptions: {
                    columns: [ 0, 1, 2, 3 ]
                },
            },
            {
                extend: 'pdfHtml5',
                className: 'btn btn-sm cb-btn-red',
                exportOptions: {
                    columns: [ 0, 1, 2, 3 ]
                },
            }
        ],
        "order": [ [0, 'desc'] ],
        columnDefs: [ { width: '18%', targets: [1, 2, 3, 4, 5] }, { width: '10%', targets: [6] } ],
        "initComplete": function() {}
    });
    tabla.draw()
}

function clean_data() {
    $(class_item).val('')
    $(class_item).selectpicker('render')
}

function reload_table() {
    $.ajax({
        method: "POST",
        url: 'usuario_list',
        dataType: 'json',
        data: {_xsrf: getCookie("_xsrf")},
        async: false,
        success: function (response) {
            load_table(response.data)
        },
        error: function (jqXHR, status, err) {
            show_message(jqXHR.responseText, 'danger', 'remove');
        }
    });
}

function obtener_persona() {
    h0 = $('#fkpersona').val()
    h1 = $('#nombre').val()
    h2 = $('#apellido').val()
    h3 = $('#ci').val()
    h4 = $('#email').val()
    h5 = $('#telefono').val()

    return add_persona(h0, h1, h2, h3, h4, h5)
}

function add_persona(h0, h1, h2, h3, h4, h5) {
    if (h0 === '') {
        return {
            'nombre': h1,
            'apellido': h2,
            'ci': h3,
            'email': h4,
            'telefono': h5
        }
    } else {
        return {
            'id': h0,
            'nombre': h1,
            'apellido': h2,
            'ci': h3,
            'email': h4,
            'telefono': h5
        }
    }
}

$('#new').click(function() {
    clean_data()
    verif_inputs('')
    validationInputSelects("modal")
    $('.item-form').parent().removeClass('focused')
    $(elem_password).attr('required', true)
    $('#div-password').removeClass('hide')

    $('#update').hide()
    $('#insert').show()
});

$('#insert').on('click', function() {
    notvalid = validationInputSelectsWithReturn("modal");

    if (!notvalid) {
        objeto = JSON.stringify({
            'username': $('#username').val(),
            'password': $('#password').val(),
            'foto': $('#foto').val(),
            'fkrol': $('#fkrol').val(),
            'persona': obtener_persona()
        })

        ajax_call('usuario_insert', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function (response) {
            self = JSON.parse(response);

            if (self.success) {
                show_msg_lg('success', self.message, 'center')
                setTimeout(function () {
                    $('#modal').modal('hide')
                    reload_table()
                }, 2000);
            }
            else show_toast('warning', self.message);
        })
    }
    else show_toast('warning', 'Por favor, ingresa todos los campos requeridos (*).');
});

function edit_item(e) {
    clean_data()
    obj = JSON.stringify({
        'id': parseInt(JSON.parse($(e).attr('data-json')))
    })
    $(elem_password).attr('required', false)
    $('#div-password').addClass('hide')

    ajax_call_get('usuario_update',{
        _xsrf: getCookie("_xsrf"),
        object: obj
    },function(response){
        var self = response.response;

        if (self.persona !== undefined) {
            $('#fkpersona').val(self.fkpersona)
            $('#nombre').val(self.persona.nombre)
            $('#apellido').val(self.persona.apellido)
            $('#ci').val(self.persona.ci)
            $('#email').val(self.persona.email)
            $('#telefono').val(self.persona.telefono)
            $('#numero').val(self.persona.numero)
        }
        $('#id').val(self.id)
        $('#username').val(self.username)
        $('#foto').val(self.foto)
        $(fkrol).val(self.fkrol)
        $(fkrol).selectpicker('render')

        clean_form()
        verif_inputs('')
        $('.item-form').parent().addClass('focused')
        $('#insert').hide()
        $('#update').show()
        $('#modal').modal('show')
    })
}

$('#update').click(function() {
    notvalid = validationInputSelectsWithReturn("modal");

    if (!notvalid) {
        objeto = JSON.stringify({
            'id': $('#id').val(),
            'username': $('#username').val(),
            'password': $('#password').val(),
            'foto': $('#foto').val(),
            'fkrol': $('#fkrol').val(),
            'persona': obtener_persona()
        })

        ajax_call('usuario_update', {
            _xsrf: getCookie("_xsrf"),
            object: objeto
        }, null, function(response) {
            self = JSON.parse(response);

            if (self.success) {
                show_msg_lg('success', self.message, 'center')
                setTimeout(function () {
                    $('#modal').modal('hide')
                    reload_table()
                }, 2000);
            }
            else show_toast('warning', self.message);
        })
    }
    else show_toast('warning', 'Por favor, ingresa todos los campos requeridos (*).');
})

function set_enable(e) {
    cb_delete = e
    b = $(e).prop('checked')

    if (!b) {
        cb_title = "¿Está seguro de que desea dar de baja el usuario?"
        cb_text = ""
        cb_type = "warning"
    } else {
        cb_title ="¿Está seguro de que desea dar de alta el usuario?"
        cb_text = ""
        cb_type = "info"
    }

    Swal.fire({
        icon: cb_type,
        title: cb_title,
        text: cb_text,
        showCancelButton: true,
        allowOutsideClick: false,
        confirmButtonColor: '#1565c0',
        cancelButtonColor: '#ef5350',
        confirmButtonText: 'Aceptar',
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.value) {
            $(cb_delete).prop('checked', !$(cb_delete).is(':checked'))

            if (b) $(cb_delete).parent().prop('title', 'Activo');
            else $(cb_delete).parent().prop('title', 'Inhabilitado');

            objeto =JSON.stringify({
                id: parseInt($(cb_delete).attr('data-id')),
                estado: b
            })

            ajax_call('usuario_state', {
                object: objeto,_xsrf: getCookie("_xsrf")}, null,
                function (response) {
                    self = JSON.parse(response)
                    icono = self.success? 'success': 'warning'
                    show_msg_lg(icono, self.message, 'center')
                    setTimeout(function() {
                        reload_table()
                    }, 2000);
                }
            )
        }
        else if (result.dismiss === 'cancel') $(cb_delete).prop('checked', !$(cb_delete).is(':checked'));
        else if (result.dismiss === 'esc') $(cb_delete).prop('checked', !$(cb_delete).is(':checked'));
    })
}

function delete_item(e) {
    Swal.fire({
        icon: "warning",
        title: "¿Está seguro de que desea eliminar permanentemente el usuario?",
        text: "",
        showCancelButton: true,
        allowOutsideClick: false,
        confirmButtonColor: '#1565c0',
        cancelButtonColor: '#ef5350',
        confirmButtonText: 'Aceptar',
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.value) {
            objeto = JSON.stringify({
                'id': parseInt(JSON.parse($(e).attr('data-json')))
            })

            ajax_call('usuario_delete', {
                object: objeto,_xsrf: getCookie("_xsrf")}, null,
                function (response) {
                    self = JSON.parse(response);

                    if (self.success) {
                        show_msg_lg('success', self.message, 'center')
                        setTimeout(function () {
                            reload_table()
                        }, 2000);
                    }
                    else show_toast('warning', self.message);
                }
            );
        }
    })
}
