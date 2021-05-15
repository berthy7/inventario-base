$(document).ready(function () {
    $.extend( true, $.fn.dataTable.defaults, {
        "language": {
            "url": "/resources/static/js/spanish.json"
        },
        dom: '<"pull-left"f><"pull-right"l>tip'
    });

    let pathname = window.location.pathname; //URL de la página
    let a = document.querySelector("a[href='"+pathname+"']");

    if (pathname !== '/') {
        let b = (a.parentNode).parentNode; //tiene LI
        let c = b.previousElementSibling; //tiene a href, elemento anterior a LI

        if (c == null) {
            b.style["display"] = "block";
        } else {
            c.classList.add('toggled');
            b.style["display"] = "block";
            a.style["background-color"] = "rgba(0,0,0,.2)";
        }
    }
    fields_keyup()
    inputmask_keyup()
});

function  salir(logo1) {
    Swal.fire({
        title: "¿Desea cerrar sesión?",
        imageUrl: logo1,
        showCancelButton: true,
        confirmButtonColor: "#0B1D50",
        cancelButtonColor: "#F44336",
        confirmButtonText: "Aceptar",
        reverseButtons: true,
        allowOutsideClick: false,
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.value) {
            Swal.fire(
                  'Gracias por tu trabajo.',
                  'Vuelve pronto.',
                  'success'
            )
            setTimeout(function () {
                window.location="/logout"
            }, 2000);
        }
    })
}
