var opts = {
    lines: 13, // The number of lines to draw
    length: 18, // The length of each line
    width: 6, // The line thickness
    radius: 9, // The radius of the inner circle
    corners: 0, // Corner roundness (0..1)
    rotate: 15, // The rotation offset
    direction: 1, // 1: clockwise, -1: counterclockwise
    color: '#000', // #rgb or #rrggbb
    speed: 0.9, // Rounds per second
    trail: 30, // Afterglow percentage
    shadow: false, // Whether to render a shadow
    hwaccel: false, // Whether to use hardware acceleration
    className: 'spinner', // The CSS class to assign to the spinner
    zIndex: 2e9, // The z-index (defaults to 2000000000)
    top: 'auto', // Top position relative to parent in px
    left: 'auto' // Left position relative to parent in px
};
var target = document.getElementById("tiny-spinner"); 
new Spinner(opts).spin(target);
