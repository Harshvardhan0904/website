function openNav() {
    document.getElementById("mySidebar").style.width = "350px";
  }
function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
  }
  document.getElementById("servicesLink").addEventListener("click", openNav);

const text = document.getElementById('text');
const trees = document.getElementById('trees');
const mount = document.getElementById('mount');
const arrow = document.getElementById('arrow')
  
window.addEventListener('scroll', () => {
    let value = window.scrollY;
    
    // Move trees downward
    trees.style.transform = `translateY(${value * 0.14}px)`;
  
    // Move mountains downward (slower than trees for parallax effect)
    mount.style.transform = `translateY(${value * 0.3}px)`;
  
    // Keep text fixed in between
    text.style.transform = `translateY(${value * 0 -100}px)`;
    arrow.style.transform = `translateY(${value * 0 -3}px)`
  });

