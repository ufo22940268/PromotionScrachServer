var isShiftPressed = false;

function checkRowInRange(from, to) {
    for (var i = from; i <= to; i ++) {
        id = "checkbox_" + i;
        $("#" + id).attr("checked", "true");
    }
}

function checkItem(cb) {
    updateSelectionState();

    if (!isShiftPressed) {
        return;
    }

    var id = cb.id;
    var cur = parseInt(id.substring(id.indexOf("_") + 1));
    var INFI = 100000;
    var nearest = INFI;
    $(".row-selector").each(function(index) {
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

function checkRow(tr) {
    console.log(tr.attr("data-id"));
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

function loadContent(page) {
    if (!page) {
        page = 1;
    }
    showLoading();
    var bankName = $("#opt-bank option:selected").val();
    var state = $("#opt-handle option:selected").val();
    var city = $("#opt-city option:selected").val();
    var url = "table.html?bank_name=" + bankName + "&state=" + state + "&page=" + page + "&city=" + city; 
    $.get(url, function(data) {
	$("#table-container").html(data);
    });

    $.get(url + "&isOption=true", function(data) {
	$("#opt-city").html(data);
    });
}
loadContent();

function sleep(milliseconds) {
    var start = new Date().getTime();
    for (var i = 0; i < 1e7; i++) {
	if ((new Date().getTime() - start) > milliseconds){
	    break;
	}
    }
}

function showLoading() {
    $("#table-container").html('<div id="spinner"></div>');
    $("#spinner").spin();
}

function showTinyLoading() {
    $("#tiny-spinner").spin('tiny', 'teal');
}

showLoading();
showTinyLoading();

function updateSelectionState() {
    if ($(".row-selector:checked").length == 0) {
        $("#select-batch-ops").css("visibility", "hidden");
    } else {
        $("#select-batch-ops").css("visibility", "visible");
    }
}

updateSelectionState();

function saveSingleOperationOnProm(item, op) {
    var id = getIdByCheckItem(item);
    startSpin(item);
    $.get("check.py?id=" + id + "&op=" + op, function(data) {
        stopSpin(item);
    });
}

function getIdByCheckItem(item) {
    return $(item).parent().attr("data-id");
}

function acceptProm(item) {
    saveSingleOperationOnProm(item, "accept");
}

function unacceptProm(item) {
    saveSingleOperationOnProm(item, "unaccept");
}

function postponeProm(item) {
    saveSingleOperationOnProm(item, "postpone");
}

function startSpin(item) {
    var spin = $(item).parent().next();
    if (spin.css("visibility") == "hidden") {
        spin.css("visibility", "visible");
    }
}

function stopSpin(item) {
    var spin = $(item).parent().next();
    if (spin.css("visibility") == "visible") {
        spin.css("visibility", "hidden");
    }
}

function saveMutibleItemStates(op) {
    $("#opt-loading").css("visibility", "visible");
    var ids = new Array();
    $(".row-selector").each(function(index) {
        if ($(this).is(":checked")) {
            ids.push($(this).attr("data-id"));
        }
    });

    var idStr = "";
    for (var i = 0; i < ids.length; i ++) {
        if (i == 0) {
            idStr += "ids=";
        }
        idStr += ids[i];
        if (i != ids.length - 1) {
            idStr += ",";
        }
    }

    var param = idStr;
    param = param + "&op=" + op;

    $.get("updateItemStates?" + param, function(data) {
        $("#opt-loading").css("visibility", "hidden");
        loadContent();
    })
}

$(document).ready(function() {
    $('#daterange').daterangepicker(
        {
            minDate: '01/01/2010',
    maxDate: '12/31/2015',
    showDropdowns: true
        }
        );

});
