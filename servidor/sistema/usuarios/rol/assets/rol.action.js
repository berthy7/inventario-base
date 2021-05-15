var class_item = '.item-form';
var id_table = '#data_table';
var class_mod = '.module';

$(document).ready( function () {
    reload_table();
});
validationKeyup("modal")

function load_table(data_tb) {
    var tabla = $(id_table).DataTable({
        destroy: true,
        data: data_tb,
        columns: [
            { title: "ID", data: "id" },
            { title: "Nombre", data: "nombre" },
            { title: "Descripción", data: "descripcion" },
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
                            <button data-json="' + data + '"  type="button" class="btn btn-primary waves-effect" title="Editar" onclick="edit_item(this)">\
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
        columnDefs: [ { width: '10%', targets: [0] }, { width: '22.5%', targets: [1, 2, 3, 4] } ],
        "initComplete": function() {}
    });
    tabla.draw()
}

function clean_data() {
    $(class_mod).prop('checked', false)
    $(class_item).val('')
}

function reload_table() {
    $.ajax({
        method: "POST",
        url: 'rol_list',
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

function analizar(parent) {
    children = $(parent).next().next().find('.module:checked')
    $(parent).prop('checked', (children.length > 0))
    grand_parent = $(parent).parent().closest('.tree-menu').prev().prev()

    if (grand_parent.length > 0) analizar(grand_parent);
}

$('.module').click(function () {
    aux = $(this).attr('id')

    if ((aux.indexOf('insert') !== -1 || aux.indexOf('update') !== -1 || aux.indexOf('delete') !== 1) && $(this).is(':checked')) {
        aux1 = aux.replace('insert', 'query')
        aux1 = aux1.replace('update', 'query')
        aux1 = aux1.replace('delete', 'query')
        $('#'+aux1).prop('checked', true)
    }

    if (aux.indexOf('query') !== -1) {
        aux1 = aux.replace('query', 'insert')
        idcmb = '#' + aux1

        $('#'+aux1).prop('checked', false)
        aux1 = aux.replace('query', 'update')
        $(idcmb).prop('checked', false)
        aux1 = aux.replace('query', 'delete')
        $(idcmb).prop('checked', false)
    }

    $(this).next().next().find('.module').prop('checked', $(this).prop('checked'))
    analizar($(this).parent().closest('.tree-menu').prev().prev())
})

function get_cb_ids(selection) {
    checkboxs_ids = []
    $(selection+':checked').each(function () {
        checkboxs_ids.push(parseInt($(this).attr('data-id')))
    })
    return checkboxs_ids
}

$('#new').click(function() {
    clean_data()
    verif_inputs('')
    validationInputSelects("modal")
    $('.item-form').parent().removeClass('focused')

    $('#update').hide()
    $('#insert').show()
});

$('#insert').on('click', function() {
    permisos = document.querySelectorAll("input[type='checkbox']:checked")
    notvalid = validationInputSelectsWithReturn("modal");

    if (!notvalid && permisos.length > 0) {
        objeto = JSON.stringify({
            'nombre': $('#nombre').val(),
            'descripcion': $('#descripcion').val(),
            'modulos': get_cb_ids('.module')
        })

        ajax_call('rol_insert', {
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

    ajax_call_get('rol_update',{
        _xsrf: getCookie("_xsrf"),
        object: obj
    },function(response){
        var self = response.response;

        $('#id').val(self.id)
        $('#nombre').val(self.nombre)
        $('#descripcion').val(self.descripcion)

        for (ic of self.modulos) {
            $('.module[data-id="' + ic.id + '"]').prop('checked', true)
        }

        clean_form()
        verif_inputs('')
        $('.item-form').parent().addClass('focused')
        $('#insert').hide()
        $('#update').show()
        $('#modal').modal('show')
    })
}

$('#update').click(function() {
    permisos = document.querySelectorAll("input[type='checkbox']:checked")
    notvalid = validationInputSelectsWithReturn("modal");

    if (!notvalid && permisos.length > 0) {
        objeto = JSON.stringify({
            'id': parseInt($('#id').val()),
            'nombre': $('#nombre').val(),
            'descripcion': $('#descripcion').val(),
            'modulos': get_cb_ids('.module')
        })

        ajax_call('rol_update', {
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
        cb_title = "¿Está seguro de que desea dar de baja el rol?"
        cb_text = "Los usuarios relacionados, también serán dados de baja."
        cb_type = "warning"
    } else {
        cb_title ="¿Está seguro de que desea dar de alta el rol?"
        cb_text = ""
        cb_type = "info"
    }

    Swal.fire({
        title: cb_title,
        text: cb_text,
        icon: cb_type,
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

            ajax_call('rol_state', {
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
        title: "¿Está seguro de que desea eliminar permanentemente el rol?",
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

            ajax_call('rol_delete', {
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
