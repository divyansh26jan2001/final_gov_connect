function sendMessage(message, itsMe) { // ...Mario
    var messageList = document.getElementById("message-list");
    
    var scrollToBottom = (messageList.scrollHeight - messageList.scrollTop - messageList.clientHeight < 80);
  
    var lastMessage = messageList.children[messageList.children.length-1];
    
    var newMessage = document.createElement("span");
    newMessage.innerHTML = message;
  
    var className;
    
    if(itsMe)
    {
      className = "me";
      scrollToBottom = true;
    }
    else
    {
      className = "not-me";
    }
    
    if(lastMessage && lastMessage.classList.contains(className))
    {
      lastMessage.appendChild(document.createElement("br"));
      lastMessage.appendChild(newMessage);
    }
    else
    {
      var messageBlock = document.createElement("div");
      messageBlock.classList.add(className);
      messageBlock.appendChild(newMessage);
      messageList.appendChild(messageBlock);
    }
    
    if(scrollToBottom)
      messageList.scrollTop = messageList.scrollHeight;
  }


// Function to retrieve the CSRF token from the cookie
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

var message = document.getElementById("message-input");

message.addEventListener("keypress", function(event) {
  var key = event.which || event.keyCode;
  
  if (key === 13 && this.value.trim() !== "") {
    var messageText = this.value.trim();
    this.value = "";

    sendMessage(messageText, true);

    // Get the CSRF token from the cookie
    var csrftoken = getCookie('csrftoken');
    
    // Make an asynchronous request to a Django view
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/answer/", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    // Set the CSRF token in the request header
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        
        // Handle the response and display it
        sendRandomMessages(response);
      }
    };
    
    var data = JSON.stringify({ "message": messageText });
    xhr.send(data);
  }
});

  // var message = document.getElementById("message-input");
  // message.addEventListener("keypress", function(event) {
  //   var key = event.which || event.keyCode;
  //   if(key === 13 && this.value.trim() !== "")
  //   {
  //     sendMessage(this.value, true);
  //     sendRandomMessages(this.value);
  //     this.value = "";
      
  //   }
  // });
  
  sendMessage("Hello!", true);
  sendMessage("Hey!", false);
  sendMessage("How are you doing?", false);
  sendMessage("I'm doing well.", true);
  sendMessage("What about you?", true);
  sendMessage("Good", false);
  
  function sendRandomMessages(message)
  {

    sendMessage(">> "+message.message, false);
  }
  
  sendRandomMessages();