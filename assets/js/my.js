var isShiftPressed = false;

function checkRowInRange(from, to) {
    for (var i = from; i <= to; i ++) {
        id = "checkbox_" + i;
        $("#" + id).attr("checked", "true");
    }
}

function batchCheck(cb) {
    if (!isShiftPressed) {
        return;
    }

    var id = cb.id;
    var cur = parseInt(id.substring(id.indexOf("_") + 1));
    var INFI = 100000;
    var nearest = INFI;
    $(":checkbox").each(function(index) {
        if ($(this).is(":checked")) {
            if (Math.abs(index - cur) < Math.abs(nearest - cur) && index != cur) {
                nearest = index;
            }
        }
    });

    if (nearest != INFI) {
        checkRowInRange(Math.min(nearest, cur), Math.max(nearest, cur));
    }
}

$(document).keydown(function (e) {
    if (e.keyCode == 16) {
        isShiftPressed = true;
    }
});

$(document).keyup(function (e) {
    if (e.keyCode == 16) {
        isShiftPressed = false;
    }
});

$("#opt-btn-accept").hover(function(options) {
    $("#opt-btn-accept").tooltip({
        title: "采纳",
    });
});

$("#opt-btn-unaccept").hover(function(options) {
    $("#opt-btn-unaccept").tooltip({
        title: "弃用",
    });
});

$("#opt-btn-skip").hover(function(options) {
    $("#opt-btn-skip").tooltip({
        title: "略过",
    });
});
