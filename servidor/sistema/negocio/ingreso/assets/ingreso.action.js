var class_item = '.item-form';
var id_table = '#data_table';
var fksucursal = document.getElementById('fksucursal');
var table_detail = document.getElementById('table_detail');
var gb_inc = 0;
var gb_prods = [];
var gb_cmbs = [];

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

function load_table(data_tb) {
    var tabla = $(id_table).DataTable({
        destroy: true,
        data: data_tb,
        columns: [
            { title: "ID", data: "id" },
            { title: "Fecha", data: "fecha" },
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
        columnDefs: [ { width: '8%', targets: [0] }, { width: '10%', targets: [1, 4, 5] }, { width: '36%', targets: [2] }, { width: '26%', targets: [3] } ],
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
        url: 'ingreso_list',
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

function event_prod(e) {
    prod = $(e).attr('data-prod')
    console.log('event SLT')
    console.log('list gb')
    console.log(gb_prods)
    console.log('list cmb')
    console.log(gb_cmbs)
    if (!gb_prods.includes($(e).val())) {
        strid = '#fkproducto' + prod
        dtcod = $(strid + ' option:selected').attr('data-codigo')
        $('#codigo' + prod).val(dtcod)

        if (gb_cmbs.includes(e.id)) {
            positm = gb_cmbs.indexOf(e.id)
            gb_prods[positm] = $(e).val()
        } else {
            gb_prods.push($(e).val())
            gb_cmbs.push(e.id)
        }
        console.log(gb_prods)
    } else {
        show_msg_lg('error', 'El producto ya esta en la lista, por favor seleccione otro.', 'center')
        $(e).val('')
        $(e).selectpicker('refresh')
        $('#codigo' + prod).val('--------')

        if (gb_cmbs.includes(e.id)) {
            console.log(gb_cmbs)
            posdel = gb_cmbs.indexOf(e.id)
            gb_prods.splice(posdel, 1)
            gb_cmbs.splice(posdel, 1)
        }
    }
    console.log('AFT list gb')
    console.log(gb_prods)
    console.log('AFT list cmb')
    console.log(gb_cmbs)
}

$('#insertar_detalle').click(function () {
    agregar_detalle('')
})

function obtener_detalle() {
    objeto = []
    objeto_inputs = $('.detalle')
    console.log(objeto_inputs)

    for (i = 0; i < objeto_inputs.length; i += 4) {
        h0 = objeto_inputs[i].value
        h1 = objeto_inputs[i + 2].value
        h2 = objeto_inputs[i + 3].value

        if (h1 !== "") {
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
    gb_prods = [];
    gb_cmbs = [];

    if ($.fn.DataTable.isDataTable('#table_detail') ) {
        tb_del = $('#table_detail').DataTable();
        tb_del.clear().draw();
    }
}

$('#new').click(function() {
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
            'detalle' : obtener_detalle()
        })
        console.log(JSON.parse(objeto))

        ajax_call('ingreso_insert', {
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

    ajax_call_get('ingreso_update',{
        _xsrf: getCookie("_xsrf"),
        object: obj
    },function(response){
        var self = response.response;

        $('#id').val(self.id)
        $('#descripcion').val(self.descripcion)
        $(fksucursal).val(self.fksucursal)
        $(fksucursal).selectpicker('render')

        for (d of self.detalle) {
            id_fkproducto = '#fkproducto' + d.id
            agregar_detalle(d.id)
            $('#id' + d.id).val(d.id)
            $(id_fkproducto).val(d.fkproducto)
            $(id_fkproducto).selectpicker('refresh')
            $('#cantidad' + d.id).val(d.cantidad)
            $(id_fkproducto).change()
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
    notvalid = validationInputSelectsWithReturn("modal");

    if (!notvalid) {
        objeto = JSON.stringify({
            'id': $('#id').val(),
            'descripcion': $('#descripcion').val(),
            'fksucursal': $('#fksucursal').val(),
            'detalle' : obtener_detalle()
        })
        console.log(JSON.parse(objeto))

        ajax_call('ingreso_update', {
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
        cb_title = "¿Está seguro de que desea dar de baja el ingreso?"
        cb_text = ""
        cb_type = "warning"
    } else {
        cb_title ="¿Está seguro de que desea dar de alta el ingreso?"
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

            ajax_call('ingreso_state', {
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
        title: "¿Está seguro de que desea eliminar permanentemente el ingreso?",
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

            ajax_call('ingreso_delete', {
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
