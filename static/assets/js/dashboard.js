$(function () {
  // $('.typeit').clearIt().typeIt('This is a sentence that was typed.', 0.06, 'text').hideCursor();

  $("#prompt-input").on("keydown", function(event) {
    if (event.which === 13) {
      event.preventDefault();
      var prompt = $(this).val();
      ragPrompt(prompt);
    }
  });
  $(".prompt-sample").on("click", function(event) {
    $('#prompt-input').val($.trim($(this).text()));
  });

  $("#prompt-submit").on("click", function(event) {
    event.preventDefault();
    var prompt = $("#prompt-input").val();
    ragPrompt(prompt);
  });

  function generateUniqueId() {
    return Math.random().toString(36).slice(2) + Date.now().toString(36).slice(2);
  }

  function ragPrompt(prompt){
    $("#prompt-input").val("");
    $('.disclaimer').hide();
    $(".prompt-zone").animate({ scrollTop: $(document).height() }, 1000);
    var msgId = "ID"+generateUniqueId();
    var msg = '<div class="c-msg user"><div class="card bg-info text-white"><div class="card-body">'+prompt+'</div></div></div><div class="c-msg assistant"><div class="card"><div class="card-body""><span id="'+msgId+'"><img height="32px" src="/static/assets/images/process.gif"/></span></div></div></div>'
    $('.chat-messages').append(msg);
    $.ajax({
      url: "/prompt", // Replace with your server-side script URL
      type: "POST",contentType: "application/json",
      dataType: "json",
      data: JSON.stringify({
        // Your data to send to the server (key-value pairs)
        "prompt": prompt
      }),
      success: function(data) {
        // Handle successful response with JSON data
        console.log("Success! Data:", data);
        
        // Access data properties using dot notation or bracket notation
        var message = data.response;
        var $response = $('.chat-messages').find('#'+msgId);
        $response.html("");
        $response.typeIt(data.response, 0.06, 'text').hideCursor();
        //alert(message);
        var nchars = data.response.length * 50;
        setTimeout(function(){
          $(".prompt-zone").animate({ scrollTop: $(document).height() }, 1000);
        }, nchars);
      },
      error: function(jqXHR, textStatus, errorThrown) {
        // Handle errors during the request
        console.log("Error:", textStatus, errorThrown);
        alert("An error occurred. Please try again later.");
      }
    });
  }

})