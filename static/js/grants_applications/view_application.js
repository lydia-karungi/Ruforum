
$("#review_form").submit(function (e) {
    e.preventDefault();
    var formData = new FormData($("#review_form")[0]);
    $.ajax({
      url: "/grantapplications/review/add/",
      type: "POST",
      data: formData,
      cache: false,
      contentType: false,
      processData: false,
      success: function (data) {
        if (data.error) {
          $("#ReviewError").html(data.error).show();
        } else {
          d = new Date(data.reviewed_on);
          $("#reviews_div").prepend("<li class='list-group-item list-row' id='review" + data.review_id + "'>" +
            "<div class='float-right right-container'>" +
            "<div class='list-row-buttons btn-group float-right'>"+
            "<button class='btn primary_btn btn-sm dropdown-toggle' data-toggle='dropdown' type='button'><span class='caret'></span>Actions</button>"+          "<ul class='dropdown-menu text-center'>" +
            "<li><a class='action' onclick='edit_review(" + data.review_id + ")'>Edit</a></li>" +
            "<li><a class='action' onclick='remove_review(" + data.review_id + ")''>Remove</a></li></ul></div></div>" +
            "<div class='stream-post-container' id='review_name"+data.review_id+"'><pre>"+data.review+"</pre></div>"+
            "<div class='stream-container'><pre class='float-left'>"+data.reviewed_by+"</pre><pre class='float-right'>"+d.toLocaleString('en-US', { hour12: true })+"</pre></div>"
          );
          $("#id_reviews").val("");
          alert("Review Submitted");
          $("#ReviewError").html('');
        }
      }
    });
  });
  
  
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