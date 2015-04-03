$(function() {
    init_link_buttons();

    init_date_input();

    init_timezone();
});

function init_timezone()
{
  var tz = jstz.determine();
  $.cookie('timezone', tz.name(), { path: '/' });
}

function init_date_input()
{
    $('.date').datetimepicker({
        pickTime: false,
        icons: {
            time: "fa fa-clock-o",
            date: "fa fa-calendar",
            up: "fa fa-arrow-up",
            down: "fa fa-arrow-down"
        }
    });

    $(".date").click(function () {
        $(this).data("DateTimePicker").show();
    });
}

function init_link_buttons()
{
    var buttons = $('.btn-form');

    buttons.click(function(e) {
        e.stopPropagation();
        e.preventDefault();

        if ($(this).hasClass('btn-delete')) {
            var x = confirm("Are you sure you want to delete?");
            if (x) {
                submit_link_button($(this));
            }
        } else {
            submit_link_button($(this));
        }
    });
}

function submit_link_button(button)
{
    var href = button.data('href'),
        url = href,
        inputs = '';
    if (href.indexOf('?') != -1) {
        var parts = href.split('?');
        url = parts[0];
        var params = parts[1].split('&');
        for(var i = 0, n = params.length; i < n; i++) {
            var pp = params[i].split('=');
            inputs += '<input type="hidden" name="' + pp[0] + '" value="' + pp[1] + '" />';
        }
    }
    $("body").append('<form action="'+url+'" method="post" id="delete-form">'+inputs+'</form>');

    $("#delete-form").submit();
}
