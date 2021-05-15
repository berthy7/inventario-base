function fields_keyup() {
    $('.form-control').keyup(function () {
        tag_element = $(this).prop('localName')

        if (['input', 'textarea'].includes(tag_element)) mensaje = 'Completa este campo'
        if (tag_element === 'select') mensaje = 'Selecciona un elemento de la lista'

        if ($(this).prop('required')) {
            if (this.value.length > 0) {
                $(this).parent().removeClass('error')
                $(this).parent().next().hide("slow", function(){ $(this).remove(); })
            } else {
                $(this).parent().addClass('error')
                if($('#errorMsg_'+$(this).attr('id')).length === 0) {
                    $('<label id="errorMsg_'+$(this).attr('id')+'" class="error text-danger">'+mensaje+'</label>').insertAfter($(this).parent()).hide().show('slow')
                }
            }
        }
    });
}

function inputmask_keyup() {
    $(".hr").focus(function () {
        $(this).parent().addClass('focused')
    })

    $('.hr').keyup(function () {
        if ($(this).prop('required')) {
            if ($(this).val().indexOf('_') === -1 && $(this).val().length > 0) {
                $(this).parent().removeClass('error')
                $(this).parent().next().hide("slow", function(){ $(this).remove(); })
            } else {
                $(this).parent().addClass('error')
                elem_next = $(this).parent().next()
                list_class = $(elem_next).prop('classList')

                if ($(elem_next).prop('localName') !== 'label') {
                    $('<label class="error text-danger">Completa este campo</label>').insertAfter($(this).parent()).hide().show('slow')
                }
            }
        }
    })
}

function printError(element, validMessage) {
    element.parentElement.classList.add("error")

    if (!document.getElementById('errorMsg_' + element.id)) {
        labelError = document.createElement("label");
        // labelError.appendChild(labelErrorText);
        labelError.setAttribute('id', "errorMsg_" + element.id)
        labelError.classList.add("error");
        labelError.classList.add("text-danger");
        labelError.innerHTML = validMessage;
        element.parentElement.insertAdjacentElement("afterend", labelError);

        setTimeout(function () {
            to_delete =document.getElementById(element.id + '-error')
            console.log(to_delete)
            if (to_delete !== null) to_delete.addClass('hide');
        }, 250)
    }
}

function eraseError(element) {
    if (document.getElementById('errorMsg_' + element.id)) {
        eleChild = document.getElementById('errorMsg_' + element.id)
        element.parentElement.classList.remove('error');
        eleChild.parentElement.removeChild(eleChild)
    }

}

function validationInputSelectsWithReturn(id) {
    var flag = false;
    var elementsInput = document.querySelectorAll('#' + id + ' input[type=text]:enabled')
    var elementsSelect = document.querySelectorAll('#' + id + ' select')
    var elementsNumber = document.querySelectorAll('#' + id + ' input[type=number]:enabled')
    var elementsTextarea = document.querySelectorAll('#' + id + ' textarea:enabled')
    var elementsEmail = document.querySelectorAll('#' + id + ' input[type=email]:enabled')
    var elementsPassword = document.querySelectorAll('#' + id + ' input[type=password]:enabled')

    for (var f = 0; f < elementsInput.length; f++) {
        if (elementsInput[f].id !== '')
            if (!elementsInput[f].checkValidity()) {
                printError(elementsInput[f], elementsInput[f].validationMessage)
                flag = true
                message = "Por favor completa el campo " + elementsInput[f].name;
                return message;
            } else {
                eraseError(elementsInput[f])
            }
    }
    for (var g = 0; g < elementsNumber.length; g++) {
        if (elementsNumber[g].id !== '')
            if (!elementsNumber[g].checkValidity()) {
                printError(elementsNumber[g], elementsNumber[g].validationMessage)
                flag = true
            } else {
                eraseError(elementsNumber[g])
            }
    }
    for (var h = 0; h < elementsTextarea.length; h++) {
        if (elementsTextarea[h].id !== '') {
            if (!elementsTextarea[h].checkValidity()) {
                printError(elementsTextarea[h], elementsTextarea[h].validationMessage)
                flag = true
                message = "Por favor completa el campo " + elementsTextarea[h].name;
                return message;
            } else eraseError(elementsTextarea[h]);
        }
    }

    for (var i = 0; i < elementsSelect.length; i++) {
        if (!elementsSelect[i].checkValidity()) {
            printError(elementsSelect[i], elementsSelect[i].validationMessage);
            flag = true;
            //return elementsSelect[i].querySelector('.bs-title-option').text;
        }
        else eraseError(elementsSelect[i]);
    }
    for (var x = 0; x < elementsPassword.length; x++) {
        if (elementsPassword[x].id !== '')
            if (!elementsPassword[x].checkValidity()) {
                printError(elementsPassword[x], elementsPassword[x].validationMessage)
                flag = true
                message = "Por favor completa el campo " + elementsPassword[x].name;
                return message;
            } else {
                eraseError(elementsPassword[x])
            }
    }
    for (var y = 0; y < elementsEmail.length; y++) {
        if (elementsEmail[y].id !== '')
            if (!elementsEmail[y].checkValidity()) {
                printError(elementsEmail[y], elementsEmail[y].validationMessage)
                flag = true
                message = "Por favor completa el campo " + elementsEmail[y].name;
                return message;
            } else {
                eraseError(elementsEmail[y])
            }
    }

    return flag
}

function verif_inputs(nombre) {
    $.each($('#form'+nombre+' .form-line input'), function (index, value) {
        if (value.value.length > 0) $(value).parent().addClass('focused');
    })
}

function validationInputSelects(id) {
    var flag = false
    var elementsInput = document.querySelectorAll('#' + id + ' input[type=text]:enabled')
    var elementsSelect = document.querySelectorAll('#' + id + ' select')
    var elementsNumber = document.querySelectorAll('#' + id + ' input[type=number]:enabled')
    var elementsTextarea = document.querySelectorAll('#' + id + ' textarea:enabled')

    for (var j = 0; j < elementsInput.length; j++) {
        if (elementsInput[j].id !== '') {
            if (!elementsInput[j].checkValidity()) {
                printError(elementsInput[j], elementsInput[j].validationMessage)
                flag = true
            }
            else eraseError(elementsInput[j]);
        }
    }

    for (var k = 0; k < elementsNumber.length; k++) {
        if (elementsNumber[k].id !== '') {
            if (!elementsNumber[k].checkValidity()) {
                printError(elementsNumber[k], elementsNumber[k].validationMessage)
                flag = true
            }
            else eraseError(elementsNumber[k]);
        }
    }

    for (var m = 0; m < elementsSelect.length; m++) {
        if (!elementsSelect[m].checkValidity()) {
            printError(elementsSelect[m], elementsSelect[m].validationMessage)
            flag = true
        }
        else eraseError(elementsSelect[m]);
    }

    for (var n = 0; n < elementsTextarea.length; n++) {
        if (elementsTextarea[n].id !== '') {
            if (!elementsTextarea[n].checkValidity()) {
                printError(elementsTextarea[n], elementsTextarea[n].validationMessage)
                flag = true
            }
            else eraseError(elementsTextarea[n]);
        }
    }

    return flag
}

function validationKeyup(id) {
    var elementsInput = document.querySelectorAll('#' + id + ' input[type=text]')
    var elementsNumber = document.querySelectorAll('#' + id + ' input[type=number]:enabled')
    var elementsPassword = document.querySelectorAll('#' + id + ' input[type=password]:enabled')
    var elementsSelect = document.querySelectorAll('#' + id + ' select')
    var elementsTextarea = document.querySelectorAll('#' + id + ' textarea')

    for (var p = 0; p < elementsInput.length; p++) {
        if (elementsInput[p].id !== '') {
            elementsInput[p].oninput = function () {
                if (!this.checkValidity()) printError(this, this.validationMessage);
                else eraseError(this);
            }
        }
    }

    for (var q = 0; q < elementsNumber.length; q++) {
        if (elementsNumber[q].id !== '') {
            elementsNumber[q].oninput = function () {
                if (!this.checkValidity()) printError(this, this.validationMessage);
                else eraseError(this);
            }
        }
    }

    for (var t = 0; t < elementsPassword.length; t++) {
        if (elementsPassword[t].id !== '') {
            elementsPassword[t].oninput = function () {
                if (!this.checkValidity()) printError(this, this.validationMessage);
                else eraseError(this);
            }
        }
    }

    for (var m = 0; m < elementsSelect.length; m++) {
        if (!elementsSelect[m].checkValidity()) {
            printError(elementsSelect[m], elementsSelect[m].validationMessage)
            flag = true
        }
        else eraseError(elementsSelect[m]);
    }

    for (var n = 0; n < elementsTextarea.length; n++) {
        if (elementsTextarea[n].id !== '') {
            if (!elementsTextarea[n].checkValidity()) {
                printError(elementsTextarea[n], elementsTextarea[n].validationMessage)
                flag = true
            }
            else eraseError(elementsTextarea[n]);
        }
    }
}

$('select.item-form').on('change', function (e) {
    console.log(e)
    console.log($(this))
    validationKeyup('modal')
});

function clean_form() {
    $('div.focused').removeClass('focused')
    $('div.error').removeClass('error')
    $('label.error').text('')
}
