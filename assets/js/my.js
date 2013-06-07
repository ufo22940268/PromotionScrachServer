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

function loadContent() {
    showLoading();
    var bankName = $("#opt-bank option:selected").val();
    var state = $("#opt-handle option:selected").val();
    $.get("table.html?bank_name=" + bankName + "&state=" + state, function(data) {
	$("#table-container").html(data);
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

$(document).ready(function() {
    $('#reportrange').daterangepicker(
	{
	    ranges: {
			'Today': [new Date(), new Date()],
	'Yesterday': [moment().subtract('days', 1), moment().subtract('days', 1)],
	'Last 7 Days': [moment().subtract('days', 6), new Date()],
	'Last 30 Days': [moment().subtract('days', 29), new Date()],
	'This Month': [moment().startOf('month'), moment().endOf('month')],
	'Last Month': [moment().subtract('month', 1).startOf('month'), moment().subtract('month', 1).endOf('month')]
		    },
	opens: 'left',
	format: 'MM/DD/YYYY',
	separator: ' to ',
	startDate: moment().subtract('days', 29),
	endDate: new Date(),
	minDate: '01/01/2012',
	maxDate: '12/31/2013',
	locale: {
	    applyLabel: 'Submit',
	fromLabel: 'From',
	toLabel: 'To',
	customRangeLabel: 'Custom Range',
	daysOfWeek: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr','Sa'],
	monthNames: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
	firstDay: 1
	},
	showWeekNumbers: true,
	buttonClasses: ['btn-danger'],
	dateLimit: false
	},
    function(start, end) {
	$('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    }
);
//Set the initial state of the picker label
$('#reportrange span').html(moment().subtract('days', 29).format('MMMM D, YYYY') + ' - ' + moment().format('MMMM D, YYYY'));

});

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
