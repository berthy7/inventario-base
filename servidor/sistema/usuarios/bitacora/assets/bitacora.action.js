$(document).ready(function () {
    reload_table();
})

function load_table(data_obj) {
    $('#data_table').DataTable({
        data: data_obj,
        responsive: true,
        columns: [
            { title: "ID", data: "id" },
            { title: "Usuario", data: "username" },
            { title: "Acción", data: "accion" },
            { title: "Dirección IP", data: "ip" },
            { title: "Fecha", data: "fecha" }
        ],
        dom: "Bfrtip",
        buttons: [
            {
                extend: 'excelHtml5',
                className: 'btn btn-sm cb-btn-teal',
                exportOptions: {
                    columns: [ 0, 1, 2, 3, 4 ]
                },
                sheetName: 'Logs',
            },
            {
                extend: 'csvHtml5',
                className: 'btn btn-sm cb-btn-info',
                exportOptions: {
                    columns: [ 0, 1, 2, 3, 4 ]
                },
            },
            {
                extend: 'pdfHtml5',
                className: 'btn btn-sm cb-btn-red',
                exportOptions: {
                    columns: [ 0, 1, 2, 3, 4 ]
                },
            }
        ],
        "order": [[ 0, 'desc' ]],
        "initComplete": function() { $('thead').addClass('thead-light') }
    });
}

function reload_table() {
    $.ajax({
        method: "POST",
        url: 'bitacora_list',
        dataType: 'json',
        data: {_xsrf: getCookie("_xsrf")},
        async: false,
        success: function (response) {
            load_table(response.data)
        },
        error: function (jqXHR, status, err) {
            show_toast('warning', jqXHR.responseText);
        }
    });
}
