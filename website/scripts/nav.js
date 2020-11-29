var fileName = location.pathname.substring(location.pathname.lastIndexOf("/") + 1);

document.writeln(
    // Nav menu
    `
    <div id="navbar">
        <nav id="main-navbar" class="navbar nav-fill navbar-expand-sm fixed-top d-none d-sm-block">
            <ul class="navbar-nav ">
                <li class="nav-item">
                    <a class="nav-link text-decoration-none" href="all_flights.html">All Flights</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link text-decoration-none" href="">Link</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link text-decoration-none" href="#">Link</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link text-decoration-none" href="#">Link</a>
                </li>
            </ul>
        </nav>
    </div>
    <div id="hamburger">
        <button id="nav-show-btn" type="button" class="btn fixed-top d-block d-sm-none">
            <nav class="material-icons icon-hamburger">menu</nav>
        </button>
    </div>
    `
    );

window.onload = function(){

    // Set navbar active page highlighting.

    // target each nav class attribute individually
    $('.navbar a').each(function() {
        if ($(this).attr('href') == fileName) 
        { 
            $(this).addClass('active'); 
            $(this).addClass('disabled'); 
    }

    document.getElementById("nav-show-btn").onclick = function() {showNav()};
    document.getElementById("content").onclick = function() {hideNav()};
    window.onresize = function() {hideNav()};
});
}

// Show navbar on mobile hamburger button click/tap.
function showNav(){
    var navbar = document.getElementById("main-navbar");
    var navShowBtn = document.getElementById("nav-show-btn")

    navbar.classList.remove("d-none", "d-sm-block");
    navShowBtn.classList.add("invisible");

    var background = document.getElementById("top-level-container");
    background.style.opacity = "0.2"
}

// Hide navbar on mobile hamburger button click/tap.
function hideNav(){
    var navbar = document.getElementById("main-navbar");
    var navShowBtn = document.getElementById("nav-show-btn")

    navbar.classList.add("d-none", "d-sm-block");
    navShowBtn.classList.remove("invisible");

    var background = document.getElementById("top-level-container");
    background.style.opacity = "1.0"
}