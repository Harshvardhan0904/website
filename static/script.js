function locoscroll() {
    gsap.registerPlugin(ScrollTrigger);

    // Using Locomotive Scroll from Locomotive https://github.com/locomotivemtl/locomotive-scroll

    const locoScroll = new LocomotiveScroll({
        el: document.querySelector("#main"),
        smooth: true
    });
    // each time Locomotive Scroll updates, tell ScrollTrigger to update too (sync positioning)
    locoScroll.on("scroll", ScrollTrigger.update);

    // tell ScrollTrigger to use these proxy methods for the "#main" element since Locomotive Scroll is hijacking things
    ScrollTrigger.scrollerProxy("#main", {
        scrollTop(value) {
            return arguments.length ? locoScroll.scrollTo(value, 0, 0) : locoScroll.scroll.instance.scroll.y;
        }, // we don't have to define a scrollLeft because we're only scrolling vertically.
        getBoundingClientRect() {
            return { top: 0, left: 0, width: window.innerWidth, height: window.innerHeight };
        },
        // LocomotiveScroll handles things completely differently on mobile devices - it doesn't even transform the container at all! So to get the correct behavior and avoid jitters, we should pin things with position: fixed on mobile. We sense it by checking to see if there's a transform applied to the container (the LocomotiveScroll-controlled element).
        pinType: document.querySelector("#main").style.transform ? "transform" : "fixed"
    });




    // each time the window updates, we should refresh ScrollTrigger and then update LocomotiveScroll. 
    ScrollTrigger.addEventListener("refresh", () => locoScroll.update());

    // after everything is set up, refresh() ScrollTrigger and update LocomotiveScroll because padding may have been added for pinning, etc.
    ScrollTrigger.refresh();
}
locoscroll();

const scroll = new LocomotiveScroll({
    el: document.querySelector('[data-scroll-container]'),
    smooth: true
});


function navAinmation() {
    var nav = document.querySelector("nav")
    nav.addEventListener('mouseenter', function () {
        var tl = gsap.timeline()
        tl.to("#nav-bottom", {
            height: "21vh"
        })
        tl.to("#nav2 h5", {
            display: "block"
        })
        tl.to("#nav2 h5 span", {
            y: 0,
            stagger: {
                amount: 0.6
            }
        })
    })

    nav.addEventListener('mouseleave', function () {
        var tl = gsap.timeline()
        tl.to("#nav2 h5 span", {
            y: 25,
            stagger: {
                amount: 0.2
            }
        })
        tl.to("#nav2  h5", {
            display: 'none',
            duration: 0.1
        })
        tl.to("#nav-bottom", {
            height: 0,
            duration: 0.2
        })

    })
}
navAinmation()

function mouseeffect(pageid, mouse) {

    var page1 = document.querySelector(pageid)
    var mouse = document.querySelector(mouse)

    page1.addEventListener("mousemove", function (dets) {
        gsap.to(mouse, {
            x: dets.x,
            y: dets.y
        })
    })

    page1.addEventListener('mouseenter', function () {
        gsap.to(mouse, {
            scale: 1
        })
    })
    page1.addEventListener('mouseleave', function () {
        gsap.to(mouse, {
            scale: 0
        })
    })
}
mouseeffect("#page1_content", "#mouse")




function spider() {
    const banner = document.querySelector("#page5");
    const canvas = document.getElementById("dots");
    const ctx = canvas.getContext("2d");

    canvas.width = banner.offsetWidth;
    canvas.height = banner.offsetHeight;

    let dots = [];
    let breakingDots = []; // Track dots affected by the click

    // Generate dots with random positions and velocities
    for (let i = 0; i < 100; i++) {
        dots.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 3 + 2,
            color: 'black',
            vx: (Math.random() - 0.5) * 0.5, // Velocity x
            vy: (Math.random() - 0.5) * 0.5, // Velocity y
        });
    }

    let mouse = { x: null, y: null };

    // Draw the dots
    const drawDots = () => {
        dots.forEach(dot => {
            ctx.fillStyle = dot.color;
            ctx.beginPath();
            ctx.arc(dot.x, dot.y, dot.size, 0, Math.PI * 2);
            ctx.fill();
        });
    };

    // Connect dots within a range
    const connectDots = () => {
        for (let i = 0; i < dots.length; i++) {
            for (let j = i + 1; j < dots.length; j++) {
                let dx = dots[i].x - dots[j].x;
                let dy = dots[i].y - dots[j].y;
                let distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 150) { // Connection range for dots
                    ctx.strokeStyle = 'rgba(44, 44, 44, 0.2)';
                    ctx.lineWidth = 0.5;
                    ctx.beginPath();
                    ctx.moveTo(dots[i].x, dots[i].y);
                    ctx.lineTo(dots[j].x, dots[j].y);
                    ctx.stroke();
                }
            }
        }
    };

    // Connect dots to the mouse pointer
    const connectToMouse = () => {
        dots.forEach(dot => {
            let dx = mouse.x - dot.x;
            let dy = mouse.y - dot.y;
            let distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 200) { // Connection range for mouse
                ctx.strokeStyle = 'rgba(0, 0, 0, 0.6)';
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(dot.x, dot.y);
                ctx.lineTo(mouse.x, mouse.y);
                ctx.stroke();
            }
        });
    };

    // Update dot positions and handle edge collisions
    const updateDots = () => {
        dots.forEach(dot => {
            dot.x += dot.vx;
            dot.y += dot.vy;

            // Bounce dots off edges
            if (dot.x < 0 || dot.x > canvas.width) dot.vx *= -1;
            if (dot.y < 0 || dot.y > canvas.height) dot.vy *= -1;
        });

        // Handle breaking dots animation
        breakingDots = breakingDots.filter(dot => {
            dot.size -= 0.2; // Shrink dot size
            return dot.size > 0; // Remove dots when size is too small
        });
    };

    // Draw breaking effect
    const drawBreakingEffect = () => {
        breakingDots.forEach(dot => {
            ctx.fillStyle = 'rgba(255, 0, 0, 0.8)';
            ctx.beginPath();
            ctx.arc(dot.x, dot.y, dot.size, 0, Math.PI * 2);
            ctx.fill();
        });
    };

    // Animation loop
    const animate = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        updateDots();
        drawDots();
        connectDots();
        if (mouse.x !== null && mouse.y !== null) connectToMouse();
        drawBreakingEffect();

        requestAnimationFrame(animate);
    };

    // Mouse events
    banner.addEventListener("mousemove", (event) => {
        mouse.x = event.pageX - banner.getBoundingClientRect().left;
        mouse.y = event.pageY - banner.getBoundingClientRect().top;
    });

    banner.addEventListener("mouseleave", () => {
        mouse.x = null;
        mouse.y = null;
    });

    banner.addEventListener("click", (event) => {
        let clickX = event.pageX - banner.getBoundingClientRect().left;
        let clickY = event.pageY - banner.getBoundingClientRect().top;

        dots.forEach(dot => {
            let dx = clickX - dot.x;
            let dy = clickY - dot.y;
            let distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 200) { // Break lines for dots within 200 range
                breakingDots.push({ ...dot, size: 5 }); // Add to breaking effect
            }
        });
    });

    // Start animation
    animate();
}

spider();

function swiper() {
    var swiper = new Swiper(".mySwiper", {
        slidesPerView: 1,
        spaceBetween: 30,
        loop: true,
        autoplay: {
            delay: 2500,
            disableOnInteraction: true
        }
    });
}
swiper()



function loader() {
    var tl = gsap.timeline()
    tl.from("#loader h1", {
        x: 20,
        opacity: 0,
        stagger: 0.2,
        duration: 0.8
    })
    tl.to("#loader h1", {
        x: 20,
        opacity: 0,
        stagger: -0.1,
        duration: 0.5
    })
    tl.to("#loader", {
        opacity: 0
    })
    tl.to("#loader", {
        display: "none"
    })

    tl.from("#page1_content h1 span", {
        y: 100,
        opacity: 0,
        stagger: 0.1,
        duration: .5
    })
}
loader()