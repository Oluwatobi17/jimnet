$(document).ready(function(){
	// Handle cursor allow when the withdraw all button is checked and vice-versa
	$('input[type="checkbox"]'). click(function(){
		if($(this).prop("checked") == true){
			$('#withbut').css({
				'cursor': 'pointer'
			})
		
			// $('.withform').attr('action', '/withdraw/all/')
		}else{
			$('#withbut').css({
				'cursor': 'not-allowed'
			})

			// $('.withform').attr('action', '/')
			// $('.withform').attr('method', 'get')
		}
	});

	$('#withbut').on('click', function(){
		$('.withdrawcontainer').toggleClass('hide')
		$('.stages').toggleClass('hide')

		amount = $(this).data('amount')
		$('#amountreq').attr('value', amount)
	})

	// Handle toggle of the nav button
	$('.dropimg').on('click', function(){
		$('#data').toggleClass('hide');
	})

	$('td .active').on('click', function(){
		$('.withdrawcontainer').toggleClass('hide')
		$('.stages').toggleClass('hide')

		amount = $(this).data('amount')
		$('#amountreq').attr('value', amount)
	})

	// Handle 
	$('.closeimg2').on('click', function(){
		$('.withdrawcontainer').toggleClass('hide')
		$('.stages').toggleClass('hide')
	})

	// Handle closing of the chart panel when the close button is click
	$('.ref').click(function(){
		$('#chartpanel').css({ 'display': 'block' })
		$('.dashcontainer').css({ 'display': 'none' })
	})

	$('#chartpanel button').click(function(){
		$('.dashcontainer').css({ 'display': 'block' })
		$('#chartpanel').css({ 'display': 'none' })
	})

	setInterval(function(){
		if($('.navbar').width() < 805){
			$('.navbar #half').removeClass('hide')
			$('.navbar #full').addClass('hide')
		}else{
			$('.navbar #full').removeClass('hide')
			$('.navbar #half').addClass('hide')
		}
	}, 100)


	// Handle nav toggel
	$('.innernavpanel a').click(function(){
		var ref = $(this).data('access')
		// Setting display:none to the active class
		$('.innernavpanel').find('.innernavshowactive').removeClass('innernavshowactive')
		$('.dashbody').find('.innernavactive').removeClass('innernavactive').addClass('hide')

		// Setting display:block to the clicked tag
		$(ref).addClass('innernavactive')
		$(ref).removeClass('hide')
		$(this).addClass('innernavshowactive')
	})

	$('.forgetpass').click(function(){
		console.log('Working for login')
		var ref = $(this).data('access')

		// Setting display:none to the active class
		$('.loginbody').find('.innernavactive').removeClass('innernavactive').addClass('hide')

		// Setting display:block to the clicked tag
		$(ref).addClass('innernavactive')
		$(ref).removeClass('hide')
	})


	// Handle drop down
	$('.infodrop .more').click(function(){
		var drop = $(this).data('drop')
		$('#'+drop).toggle(10, function(){
			
		})
	})

	$('.infodrop2 .more').click(function(){

		var drop = $(this).data('drop')
		$('#'+drop).toggle(10, function(){

			// if ($(this).data('plus')){
			// 	$(this).text('+')
			// }else{
			// 	$(this).text('-')
			// }
		})
	})

	$('form .changepass').on('click', function(){
		var act = $(this).data('act')
		if (act=='pin'){
			$('.pin').addClass('hide')
			$('.pass').removeClass('hide')
		}else if (act=='pass'){
			$('.pass').addClass('hide')
			$('.pin').removeClass('hide')
		}
	})

})