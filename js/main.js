$( document ).ready(function() {
	$('.nav__toggler').click(function (){
		$('.nav').toggleClass('active');
		$('.nav__icone').toggleClass('active');
		$('.nav-list').toggleClass('active');
	});

    gsap.registerPlugin(ScrollTrigger);

    gsap.from(".main__heading", {
        duration: 1,
        y: -100,
        opacity: 0,
        ease: "power4.out",
        stagger: 0.2
    });

    gsap.from(".services-box", {
        scrollTrigger: ".services-box",
        duration: 1,
        y: 100,
        opacity: 0,
        ease: "power4.out",
        stagger: 0.2
    });

    gsap.from(".about-us-box", {
        scrollTrigger: ".about-us-box",
        duration: 1,
        x: -100,
        opacity: 0,
        ease: "power4.out",
        stagger: 0.2
    });

    gsap.from(".projects-box", {
        scrollTrigger: ".projects-box",
        duration: 1,
        y: 100,
        opacity: 0,
        ease: "power4.out",
        stagger: 0.2
    });
});