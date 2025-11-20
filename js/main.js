$( document ).ready(function() {
	// Mobile menu toggle
	$('.nav__toggler').click(function (){
		$('.nav').toggleClass('active');
		$('.nav__icone').toggleClass('active');
		$('.nav-list').toggleClass('active');
	});

	// AOS Initialization
	AOS.init({
		offset: 100,
		duration: 1000,
		once: true, // Only animate once
		easing: 'ease-out-cubic'
	});

	// Add scrolled class to nav on scroll
	$(window).scroll(function() {
		if ($(this).scrollTop() > 50) {
			$('.nav').addClass('scrolled');
		} else {
			$('.nav').removeClass('scrolled');
		}
	});

	// Smooth scroll for internal links (if any)
	$('a[href*="#"]').on('click', function(e) {
		e.preventDefault();
		$('html, body').animate(
			{
				scrollTop: $($(this).attr('href')).offset().top,
			},
			500,
			'linear'
		);
	});
});
