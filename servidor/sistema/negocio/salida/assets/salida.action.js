var class_item = '.item-form';
var id_table = '#data_table';
var fksucursal = document.getElementById('fksucursal');
var fkcliente = document.getElementById('fkcliente');
var table_detail = document.getElementById('table_detail');

$(document).ready( function () {
    reload_table();
});
validationKeyup("modal")

$('#fksucursal').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar sucursal',
    title: 'Seleccione una sucursal'
})

$('#fkcliente').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar cliente',
    title: 'Seleccione un cliente'
})

function load_table(data_tb) {
    var tabla = $(id_table).DataTable({
        destroy: true,
        data: data_tb,
        columns: [
            { title: "ID", data: "id" },
            { title: "Fecha", data: "fecha" },
            { title: "Cliente", data: "cliente" },
            { title: "Descripción", data: "descripcion",
                render: function(data, type, row) {
                    return '<div style="white-space: pre-wrap">' + data + '</div>'
                }
            },
            { title: "Sucursal", data: "sucursal" },
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
                    columns: [ 0, 1 ]
                },
                sheetName: 'Logs',
            },
            {
                extend: 'csvHtml5',
                className: 'btn btn-sm cb-btn-info',
                exportOptions: {
                    columns: [ 0, 1 ]
                },
            },
            {
                extend: 'pdfHtml5',
                className: 'btn btn-sm cb-btn-red',
                exportOptions: {
                    columns: [ 0, 1 ]
                },
            }
        ],
        "order": [ [0, 'desc'] ],
        columnDefs: [ { width: '8%', targets: [0] }, { width: '10%', targets: [1, 5, 6] }, { width: '15%', targets: [2, 4] }, { width: '32%', targets: [3] } ],
        "initComplete": function() {}
    });
    tabla.draw()
}

function load_detail() {
    obj = JSON.stringify({
        'idsucursal': parseInt($(fksucursal).val())
    })
    $.ajax({
        method: "POST",
        url: 'inventario_by_sucursal',
        dataType: 'json',
        data: {
            _xsrf: getCookie("_xsrf"),
            object: obj
        },
        async: false,
        success: function (response) {
            $('#table_detail').DataTable({
                destroy: true,
                data: response.data,
                columns: [
                    { title: "Código", data: "codigo" },
                    { title: "Producto", data: "producto" },
                    { title: "Cantidad actual", data: "cantidad" },
                    { title: "Cantidad salida", data: "fkproducto",
                        render: function(data, type, row) {
                            return '\
                                 <div class="form-group form-float">\
                                    <div class="form-line">\
                                        <input type="hidden" id="id' + data + '" name="id' + data + '" class="detalle">\
                                        <input type="hidden" id="fkproducto' + data + '" name="fkproducto' + data + '" class="item-form detalle" value="' + row.fkproducto + '">\
                                        <input type="number" onkeyup="event_cantidad(this)" min="0" max="' + row.cantidad + '" id="cantidad' + data + '" name="cantidad' + data + '" class="form-control cantidad detalle">\
                                        <label for="cantidad' + data + '" class="form-label"></label>\
                                    </div>\
                                </div>'
                        }
                    },
                ],
                "order": [ [0, 'asc'] ],
                columnDefs: [ {width: '12%', targets: [0]}, {width: '60%', targets: [1]}, {width: '14%', targets: [2, 3]} ],
            });
        },
        error: function (jqXHR, status, err) {
            show_message(jqXHR.responseText, 'danger', 'remove');
        }
    });
}

function clean_data() {
    $(class_item).val('')
    $(class_item).selectpicker('render')
}

function reload_table() {
    $.ajax({
        method: "POST",
        url: 'salida_list',
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

function obtener_detalle() {
    objeto = []
    objeto_inputs = $('.detalle')
    console.log(objeto_inputs)

    for (i = 0; i < objeto_inputs.length; i += 3) {
        h0 = objeto_inputs[i].value
        h1 = objeto_inputs[i + 1].value
        h2 = objeto_inputs[i + 2].value

        if (h2 !== "" && parseInt(h2) > 0) {
            objeto.push((function add_objeto(h0, h1, h2) {
                if (h0 === '') {
                    return {
                        'fkproducto': h1,
                        'cantidad': h2
                    }
                } else {
                    return {
                        'id': h0,
                        'fkproducto': h1,
                        'cantidad': h2
                    }
                }
            })(h0, h1, h2))
        }
    }
    return objeto
}

function clean_table() {
    if ($.fn.DataTable.isDataTable('#table_detail') ) {
        tb_del = $('#table_detail').DataTable();
        tb_del.clear().draw();
    }
}

$(fksucursal).on('change', function () {
    if (!['', null].includes($(this).val())) load_detail();
});

function event_cantidad(e) {
    console.log($(e).attr('id'))
    console.log($(e).val())
    console.log($(e).attr('max'))
    if (!['', null].includes($(e).val())) {
        if (parseInt($(e).val()) > parseInt($(e).attr('max'))) $(e).val($(e).attr('max'));
    }
}

$('#new').on('click', function() {
    clean_data()
    verif_inputs('')
    validationInputSelects("modal")
    $('.item-form').parent().removeClass('focused')
    clean_table()

    $('#update').hide()
    $('#insert').show()
});

$('#insert').on('click', function() {
    notvalid = validationInputSelectsWithReturn("modal");

    if (!notvalid) {
        objeto = JSON.stringify({
            'descripcion': $('#descripcion').val(),
            'fksucursal': $('#fksucursal').val(),
            'fkcliente': $('#fkcliente').val(),
            'detalle' : obtener_detalle()
        })
        console.log(JSON.parse(objeto))

        ajax_call('salida_insert', {
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
    clean_table()
    obj = JSON.stringify({
        'id': parseInt(JSON.parse($(e).attr('data-json')))
    })

    ajax_call_get('salida_update',{
        _xsrf: getCookie("_xsrf"),
        object: obj
    },function(response){
        var self = response.response;

        $('#id').val(self.id)
        $('#descripcion').val(self.descripcion)
        $(fksucursal).val(self.fksucursal)
        $(fksucursal).selectpicker('render')
        $(fksucursal).change()
        $(fkcliente).val(self.fkcliente)
        $(fkcliente).selectpicker('render')

        setTimeout(function () {
            for (d of self.detalle) {
                console.log(d.fkproducto)
                console.log(d.id)
                console.log(d.cantidad)
                $('#id' + d.fkproducto).val(d.id)
                $('#cantidad' + d.fkproducto).val(d.cantidad)
            }
        }, 1000);
        
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
            'descripcion': $('#descripcion').val(),
            'fksucursal': $('#fksucursal').val(),
            'fkcliente': $('#fkcliente').val(),
            'detalle' : obtener_detalle()
        })
        console.log(JSON.parse(objeto))

        ajax_call('salida_update', {
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
        cb_title = "¿Está seguro de que desea dar de baja la salida?"
        cb_text = ""
        cb_type = "warning"
    } else {
        cb_title ="¿Está seguro de que desea dar de alta la salida?"
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

            ajax_call('salida_state', {
                object: objeto, _xsrf: getCookie("_xsrf")}, null,
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
        title: "¿Está seguro de que desea eliminar permanentemente la salida?",
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

            ajax_call('salida_delete', {
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
