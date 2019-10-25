function build_alert(type, msg) {
    var pre = '<div id="main-alert" class="alert alert-'+type+' alert-dismissible fade show" role="alert">'
    var post = '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
    $("#content-container").prepend(pre+msg+post)
}

$(document).ready(function() {
    $(".remove-job-button").on("click", function(event) {
        var job_id = $(this).attr("data-job-id");
        var endpoint = $(this).attr("data-remove-endpoint");
        $.ajax({
            url: endpoint,
            type: "GET"
        })
        .done(function(data) {
            build_alert("success", data);
            setTimeout(function(){
                $("#job-"+job_id+"-row").remove();
            }, 1000);
        })
        .fail(function(data) {
            build_alert("danger", data);
        })
        .always(function(data) {
            $("#remove-job-"+job_id+"-modal").modal("hide");
        });
    });
});