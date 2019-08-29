// document.addEventListener('DOMContentLoaded', function() {
//     const mb = document.querySelectorAll('.materialboxed');
// 	M.Materialbox.init(mb, {});
//   });

document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.querySelectorAll('.carousel');
    M.Carousel.init( carousel, {
    	indicators: true,
    	fullWidth: true
  	});
  });