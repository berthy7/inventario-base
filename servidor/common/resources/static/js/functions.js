function ajax_call(url, data, render, callback) {
    $.ajax({
        method: "POST",
        url: url,
        data: data,
        success: function (response) {
            if (render != null) $(render).html(response);
            if (callback != null) callback(response);
        },
        error: function (jqXHR, status, err) {
            show_message(jqXHR.responseText, 'danger', 'remove');
        }
    });
}

function ajax_call_get(url, data, callback) {
    $.ajax({
        method: "PUT",
        url: url,
        data: data,
        success: function (response) {
            if (callback != null) {
                dictionary = JSON.parse(response)
                callback(dictionary)
            }
        },
        error: function (jqXHR, status, err) {
            show_message('Error', jqXHR.responseText, 'danger', 'remove')
        }
    });
}

function ajax_call_login(url, data, callback) {
    $.ajax({
        method: "POST",
        url: url,
        data: data,
        success: function (response) {
            dictionary = JSON.parse(response)

            if (callback != null) callback(dictionary)
        },
        error: function (jqXHR, status, err) {
            show_message(jqXHR.responseText, 'danger', 'remove')
        }
    });
}
