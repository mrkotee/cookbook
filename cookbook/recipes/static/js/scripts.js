$(document).ready(function () {
  // Activate WOW.js
  new WOW().init();
});

$(window).ready(function() {
  // Splash Screen
  $("#splash").fadeOut();
});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function ajax_search(search_dict) {
    var result = $.post("search/",
        search_dict,
    );
    return result;
};

function recipes_search_main() {
    recipe_title = $("input[name='recipe_part_name']")[0].value
    selected_ingredient = $("select[name='ingredient']")[0].value
    search_dict = {
        "recipe_title": recipe_title,
        "ingredient": selected_ingredient,
    };
    var posting = ajax_search(search_dict);
    posting.done( function (data) {
        $("#recipe_items").html(data);
    });
};


$(document).on('change', ".search", function () {
    recipes_search_main()
});

