var mediaQuery = window.matchMedia('(max-width: 46.1875em)');
if (mediaQuery.matches) {
    var contents = document.getElementsByClassName("post-content");
    for (var i = 0; i < contents.length; i++) {
        var content = contents[i].innerHTML;
        if (content.length > 40) {
            content = content.substring(0, 32) + "...";
            contents[i].innerHTML = content;
        }
    }

    var noti_icon = document.querySelector(".nav_noti")
    var nav_edit =document.querySelector(".nav_edit")

    var blog_page = document.querySelector(".blog-page")
    var home_page = document.querySelector(".home-page")
    var noti_page = document.querySelector(".notification")


    noti_icon.addEventListener("click", function() {

        var isClosed = noti_page.style.display !== 'flex';
        if (isClosed){
          noti_page.style.display = 'flex';
        }
    })

    nav_edit.addEventListener("click", function() {
        if(home_page.classList.contains("none")) {
            home_page.classList.remove("none")
        }
        var isClosed = blog_page.style.display !== 'flex';
        if (isClosed){
          blog_page.style.display = 'flex';
        }
    })
}