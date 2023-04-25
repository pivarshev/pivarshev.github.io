var my_element = document.getElementById("my_element");

my_element.scrollIntoView({
  behavior: "smooth",
  block: "start",
  inline: "nearest"
});

function hover(element) {
    element.setAttribute("src", "images/IMG_0009.PNG")
}

function unhover(element) {
    element.setAttribute("src", "images/IMG_0008.PNG")
}

setTimeout(function(){
    $("#loading").addClass("animated fadeOut");
    setTimeout(function(){
      $("#loading").removeClass("animated fadeOut");
      $("#loading").css("display","none");
    },800);
},1650);

$(document).ready(function(){
    $("a").on('click', function(event) {
      if (this.hash !== "") {
        event.preventDefault();
        var hash = this.hash;
        $('body,html').animate({
        scrollTop: $(hash).offset().top
        }, 1800, function(){
        window.location.hash = hash;
       });
       } 
      });
  });
  