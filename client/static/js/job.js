function toggle_trigger_box(type) {
    if (type === "cron") {
        console.log("Cron Selected");
        $(".trigger-args-boxes").hide();
        $("#cron-trigger-args-box").show();
    } else if (type === "date") {
        console.log("Date Selected");
        $(".trigger-args-boxes").hide();
        $("#date-trigger-args-box").show();
    } else if (type === "interval") {
        console.log("Interval Selected");
        $(".trigger-args-boxes").hide();
        $("#interval-trigger-args-box").show();
    } else {
        console.log("Unknown Trigger Type");
        $(".trigger-args-boxes").hide();
    }
}

$(document).ready(function() {
    var trigger_type = $(".trigger:checked").val();
    if ($(".trigger:checked").val()) {
        $(".trigger:checked").parent().addClass("active")
    }
    toggle_trigger_box(trigger_type);
    $(".trigger").on("change", function(event) {
        var trigger_type = $(this).val();
        toggle_trigger_box(trigger_type);
    });
}).on("submit", "#job", function(event) {
    // Check Every Datetime Field
    $("input[type=datetime-local][step=1]").each(function(index, el) {
        if (($(this).val().match(/:/g) || []).length < 2) { // If Second is 0
            $(this).val(function() {
                return this.value + ":00"; // Add Second Paddings
            })
        }
    });
});;