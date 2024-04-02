var mediaQuery = window.matchMedia('(min-width: 46.25em) and (max-width: 63.9375em)');
if (mediaQuery.matches) {
    var contents = document.getElementsByClassName("post-content");
    for (var i = 0; i < contents.length; i++) {
        var content = contents[i].innerHTML;
        if (content.length > 48) {
            content = content.substring(0, 59) + "...";
            contents[i].innerHTML = content;
        }
    }

    var noti_icon = document.querySelector(".nav_noti")
    var nav_edit =document.querySelector(".nav_edit")

    var blog_page = document.querySelector(".blog-page")
    var home_page = document.querySelector(".home-page")
    var blog_noti = document.querySelector(".blog-noti")

    if(!blog_page.classList.contains("none")) {
        blog_page.classList.add("none")
    }

    if(!blog_noti.classList.contains("none")) {
        blog_noti.classList.add("none")
    }

    noti_icon.addEventListener("click", function() {
        console.log(noti_icon)
        console.log(blog_page)
        console.log(home_page)
        console.log(blog_noti)
        console.log(nav_edit)

        if(blog_noti.classList.contains("none")) {
            blog_noti.classList.remove("none")
            if(!blog_page.classList.contains("none")) {
                blog_page.classList.add("none")
            }
            if(!home_page.classList.contains("none")) {
                home_page.classList.add("none")
            }
            if(document.querySelector(".notification").classList.contains("none")) {
                document.querySelector(".notification").classList.remove("none")
            }
        } else {
            if(document.querySelector(".notification").classList.contains("none")) {
                document.querySelector(".notification").classList.remove("none")
            }
        }
    })

    nav_edit.addEventListener("click", function() {
        if(blog_page.classList.contains("none")) {
            blog_page.classList.remove("none")
            if(!blog_noti.classList.contains("none")) {
                blog_noti.classList.add("none")
            }
            if(!home_page.classList.contains("none")) {
                home_page.classList.add("none")
            }
            if(!document.querySelector(".notification").classList.contains("none")) {
                document.querySelector(".notification").classList.add("none")
            }
        } else {
            if(!blog_noti.classList.contains("none")) {
                blog_noti.classList.add("none")
            }
            if(!home_page.classList.contains("none")) {
                home_page.classList.add("none")
            }
            if(!document.querySelector(".notification").classList.contains("none")) {
                document.querySelector(".notification").classList.add("none")
            }
        }
    })
}
