const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    onOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
})

function show_toast(category, message, posicion='top-end') {
    Toast.fire({ icon: category, title: message, position: posicion })
}

function show_msg_lg(icono, mensaje, posicion) {
    Swal.fire({
      position: posicion,
      icon: icono,
      title: mensaje,
      showConfirmButton: false,
      timer: 2000
    })
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
