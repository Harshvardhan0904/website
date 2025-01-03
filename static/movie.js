function openNav() {
    document.getElementById("mySidebar").style.width = "350px";
  }
function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
  }
  document.getElementById("servicesLink").addEventListener("click", openNav);