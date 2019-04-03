
$(document).ready(function(){
	// Handle cursor allow when the withdraw all button is checked and vice-versa
	$('input[type="checkbox"]'). click(function(){
		if($(this).prop("checked") == true){
			$('#withbut').css({
				'cursor': 'pointer'
			})
		}else{
			$('#withbut').css({
				'cursor': 'not-allowed'
			})
		}
	})

	// Handle toggle of the nav button
	$('.dropimg').on('click', function(){
		$('#data').toggleClass('hide');
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
		if($('.navbar').width() < 711){
			$('.navbar #half').removeClass('hide')
			$('.navbar #full').addClass('hide')
		}else{
			$('.navbar #full').removeClass('hide')
			$('.navbar #half').addClass('hide')
		}
	}, 1000)


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


	// Handle drop down
	$('.infodrop .more').click(function(){
		var drop = $(this).data('drop')
		$('#'+drop).toggle(10, function(){
			
		})
	})

	// var drop = $('.infodrop .more').attr('id')
	// drop = drop.replace('C', '')
	// $('#'+drop).css({ 'display': 'inline' })

})