$("#new-pdf").on("click", function(){
  $("#step1").css("display", "block");
    $("#step2").css("display", "none");
    $("#txt").html("");
    $("#references").html("");
    $('.progress-bar').text('0%');
    $('.progress-bar').width('0%');
    $('#files-to-upload').val("");
});
$('code').click(function(ev) {
  SelectText(ev.target.id);
});
