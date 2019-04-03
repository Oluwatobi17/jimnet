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
	})

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

	// Handling admin process button process
	$('.processbut').on('click', function(){
		var id = $(this).data('pk')
		$.ajax({
			url: '/jimcontrol/admin/processrequest/'+id,
			method: 'get',
			success: function(data){
				console.log('That was successful')
				$('#'+id).removeClass('active').removeClass('processbut')
				$('#'+id+'status').text('Processed')
			},
			error: function(err){
				$('#reactmessage').removeClass('hide')
				$('#reactmessage').text('An error occured!')
			}
		})
	})

	// Handling admin process button process
	$('.staffprocessbut').on('click', function(){
		var id = $(this).attr('id')
		console.log('Id is ')
		console.log(id)
		$.ajax({
			url: '/jimcontrol/staff/processrequest/'+id,
			method: 'get',
			success: function(data){
				console.log('That was successful')
				$('#'+id).removeClass('active').removeClass('processbut')
				$('#'+id+'status').text('Processed')
			},
			error: function(err){
				console.log(err)
				$('#reactmessage').removeClass('hide')
				$('#reactmessage').text('An error occured!')
			}
		})
	})

	$('#clearRequest').on('click', function(){
		var id = $(this).data('job')
		$.ajax({
			url: '/jimcontrol/staff/clearrequests/'+id,
			method: 'get',
			success: function(data){
				$('#'+id).removeClass('active').removeClass('processbut')
				$('#'+id+'status').text('Processed')
			},
			error: function(err){
				$('#reactmessage').removeClass('hide')
				$('#reactmessage').text('An error occured!')
			}
		})
	})

	$('.actionbut').on('click', function(){
		
		var id = $(this).attr('id')
		id = id.replace('sus', '')
		var work = $(this).data('work')
		if (work=='suspend'){
			$.ajax({
				url: '/jimcontrol/admin/suspendstaff/'+id,
				method: 'get',
				success: function(data){
					$('#sus'+id).text('Allow')
					$('#sus'+id).data('work', 'allow')
				},
				error: function(err){
					$('#reactmessage').removeClass('hide')
					$('#reactmessage').text('An error occured!')
				}
			})
		}else{
			$.ajax({
				url: '/jimcontrol/admin/allowstaff/'+id,
				method: 'get',
				success: function(data){
					$('#sus'+id).text('Suspend')
					$('#sus'+id).data('work', 'suspend')
				},
				error: function(err){
					$('#reactmessage').removeClass('hide')
					$('#reactmessage').text('An error occured!')
				}
			})
		}
		
	})

})
