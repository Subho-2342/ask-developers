/* ================= NAVBAR SCROLL ================= */
window.addEventListener("scroll", () => {
    document.querySelector(".navbar")
    .classList.toggle("scrolled", window.scrollY > 50);
});


/* ================= TYPING EFFECT ================= */
const texts = [
    "Industrial Land Experts",
    "Factory & Warehouse Deals",
    "Premium Investment Properties"
];

let textIndex = 0;
let charIndex = 0;
let isDeleting = false;

function typeEffect(){
    const typingEl = document.getElementById("typing");
    const currentText = texts[textIndex];

    if(isDeleting){
        charIndex--;
    } else {
        charIndex++;
    }

    typingEl.innerHTML = currentText.substring(0, charIndex);

    let speed = isDeleting ? 40 : 80;

    if(!isDeleting && charIndex === currentText.length){
        speed = 1500; // pause
        isDeleting = true;
    } 
    else if(isDeleting && charIndex === 0){
        isDeleting = false;
        textIndex = (textIndex + 1) % texts.length;
        speed = 300;
    }

    setTimeout(typeEffect, speed);
}

/* ================= HERO SLIDER ================= */
document.addEventListener("DOMContentLoaded", () => {

    const slides = document.querySelectorAll('.slide');

    if(slides.length === 0) return; // safety

    let current = 0;

    function showSlide(index){
        slides.forEach(slide => slide.classList.remove('active'));
        slides[index].classList.add('active');
    }

    function nextSlide(){
        current = (current + 1) % slides.length;
        showSlide(current);
    }

    /* SHOW FIRST SLIDE IMMEDIATELY */
    showSlide(current);

    /* START SLIDER AFTER SMALL DELAY (IMPORTANT) */
    setTimeout(() => {
        setInterval(nextSlide, 5000);
    }, 800);

});


/* ================= PRELOAD EXTRA IMAGES ================= */
const extraImages = [
    "img/slide4.jpg",
    "img/slide5.jpg",
    "img/slide6.jpg",
    "img/slide7.jpg"
];

extraImages.forEach(src => {
    const img = new Image();
    img.src = src;
});


/* ================= MOBILE MENU ================= */
const menuToggle = document.getElementById("menuToggle");
const navMenu = document.getElementById("navMenu");

// TOGGLE MENU
menuToggle.addEventListener("click", () => {
    navMenu.classList.toggle("active");
    menuToggle.classList.toggle("open");
});

// CLOSE MENU WHEN CLICK LINK (🔥 PREMIUM UX)
document.querySelectorAll("#navMenu a").forEach(link => {
    link.addEventListener("click", () => {
        navMenu.classList.remove("active");
        menuToggle.classList.remove("open");
    });
});


/* ================= TYPING ================= */
document.addEventListener("DOMContentLoaded", () => {
    typeEffect();
});
window.addEventListener("scroll", () => {
  const about = document.querySelector(".about-box");
  const pos = about.getBoundingClientRect().top;

  if(pos < window.innerHeight - 100){
    about.classList.add("active");
  }
});

const office = document.querySelector(".office-container");

window.addEventListener("scroll", () => {
    const trigger = window.innerHeight * 0.85;
    const top = office.getBoundingClientRect().top;

    if(top < trigger){
        office.classList.add("active");
    }
});

const services = document.querySelector(".grid");

window.addEventListener("scroll", () => {
    const trigger = window.innerHeight * 0.85;
    const top = services.getBoundingClientRect().top;

    if(top < trigger){
        services.classList.add("active");
    }
});
/* ================= FILTER ================= */

/* ================= FILTER ================= */

const filterBtns = document.querySelectorAll(".project-filters button");
const cards = document.querySelectorAll(".project-card");

filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {

        filterBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        let filter = btn.dataset.filter;

        cards.forEach(card => {

            if (filter === "all" || card.classList.contains(filter)) {
                card.style.display = "flex"; // ✅ FIXED (not block)
            } else {
                card.style.display = "none";
            }

        });
    });
});


/* ================= MODAL ================= */

const modal = document.getElementById("projectModal");
const modalImg = document.getElementById("modalImg");
const modalTitle = document.getElementById("modalTitle");
const modalDesc = document.getElementById("modalDesc");
const modalStatus = document.getElementById("modalStatus");

// ✅ FIXED CLASS NAME
const closeBtn = document.querySelector(".close-btn");

cards.forEach(card => {
    card.addEventListener("click", () => {

        modal.classList.add("active");

        modalImg.src = card.dataset.img;
        modalTitle.textContent = card.dataset.title;
        modalDesc.textContent = card.dataset.desc;

        modalStatus.textContent = card.dataset.status;

        // RESET CLASS
        modalStatus.className = "modal-status";

        if (card.classList.contains("completed")) {
            modalStatus.classList.add("completed");
        } else {
            modalStatus.classList.add("under");
        }

    });
});


/* ================= CLOSE MODAL ================= */

// CLOSE BUTTON
closeBtn.addEventListener("click", () => {
    modal.classList.remove("active");
});

// CLICK OUTSIDE
modal.addEventListener("click", (e) => {
    if (e.target === modal) {
        modal.classList.remove("active");
    }
});

const topBtn = document.getElementById("topBtn");

window.addEventListener("scroll", () => {
    if(window.scrollY > 300){
        topBtn.classList.add("show");
    }else{
        topBtn.classList.remove("show");
    }
});

topBtn.onclick = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
};

document.addEventListener("DOMContentLoaded", () => {

    emailjs.init("whDjuYbo3KR389Eso");

    const contactForm = document.getElementById("contact-form");

    console.log(contactForm);

    if(contactForm){

        contactForm.addEventListener("submit", function(event){

            event.preventDefault();

            emailjs.sendForm(
                "service_p57ze38",
                "template_17y7myk",
                this
            )

            .then(() => {

                alert("Message Sent Successfully!");

                contactForm.reset();

            })

            .catch((error) => {

                alert("Failed To Send Message");

                console.log(error);

            });

        });

    }

});