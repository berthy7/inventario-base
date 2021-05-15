function show_message(mensaje, tipo, icono){
    $.notify({
        icon: 'glyphicon glyphicon-ok',
        message: mensaje
    },{
        type: tipo,
        allow_dismiss: false,
        placement: {
            from: "bottom",
            align: "center"
        },
        delay: 1000,
        timer: 1000,
        mouse_over: null,
        animate: {
            enter: 'animated fadeInDown',
            exit: 'animated fadeOutUp'
        },
        template: '\
            <div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">\
                <span class = "glyphicon glyphicon-'+icono+'"> </span>\
                <span data-notify="message">{2}</span>\
            </div>'
    });
 }
