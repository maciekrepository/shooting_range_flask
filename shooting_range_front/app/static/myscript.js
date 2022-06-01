
		window.addEventListener('scroll', function(){
			const header = document.querySelector('header');
			header.classList.toggle("sticky", window.scrollY > 0);
			});

			function toggleMenu(){
			const MenuToggle=document.querySelector('.MenuToggle');
			const navigation = document.querySelector('.navigation');
			MenuToggle.classList.toggle('active');
			navigation.classList.toggle('active');
			}
