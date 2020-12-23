
  function edit_review(x) {
    $("#Reviews_Cases_Modal").modal("show");
    review = $("#review_name" + x).text();
    $("#reviewid").val(x);
    $("#id_editreview").val(review);
  }
  
  $("#review_edit").click(function (e) {
    e.preventDefault();
    var formData = new FormData($("#review_edit_form")[0]);
    $.ajax({
      url: "/grants_applications/review/edit/",
      type: "POST",
      data: formData,
      cache: false,
      contentType: false,
      processData: false,
      success: function (data) {
        if (data.error) {
          $("#ReviewEditError").html(data.error).show();
        } else {
          $("#review_name" + data.review_id).html("<pre>" + data.review + "</pre>");
          $("#Reviews_Cases_Modal").modal("hide");
          $("#id_editreview").val("");
          $("#ReviewEditError").html("");
        }
      }
    });
  });
  
  
  function HideError(e) {
    $("#ReviewError").hide();
  }
  
  function remove_review(x) {
    var con = confirm("Do you want to Delete it for Sure!?");
    if (con == true) {
      $.post("/grants_applications/review/remove/", {
        "review_id": x
      }, function (data) {
        if (data.error) {
          alert(data.error);
        } else {
          $("#review" + data.cid).remove();
        }
      })
    }
  }