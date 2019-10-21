$(document).ready(function(){
	// Handling withdraw process button 'process'
	$('.staffprocessbut').on('click', function(){
		var id = $(this).attr('id')
		$.ajax({
			url: '/jimcontrol/staff/processrequest/'+id,
			method: 'get',
			success: function(data){
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

	// Mark complain
	$('.actionbut').on('click', function(){
		var id = $(this).attr('id').replace('mark', '')
		var mark = $(this).data('work')

		$.ajax({
			url: '/jimcontrol/staff/complain/'+mark+'/' + id,
			method: 'get',
			success: function(data){
				if(mark=='read'){
					$('#mark'+id).text('Mark Unread')
					$('#mark'+id).data('work', 'unread')
					$('#not'+id).text('Read')
				}else{
					$('#mark'+id).text('Mark Read')
					$('#mark'+id).data('work', 'read')
					$('#not'+id).text('Unread')
				}
				
			},
			error: function(err){
				console.log(err)
				$('#reactmessage').removeClass('hide')
				$('#reactmessage').text('An error occured!')
			}
		})
	})

	// Clean withdraw request
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

	// For activating a booked user in Staff (Agent)
	$('#agent').delegate('.active_agent','click', function(){
		var balance = $('.right .balance').text()
		if (balance<100){
			alert('You have insufficient balance')
			return;
		}
		var self = $(this)
		$(this).undelegate('click')
		$.ajax({
			url: '/api/activate/' + self.data('user'),
			method: 'get',
			success: function(data){
				if(data){
					self.closest('.infodrop').remove()
					$('.right .balance').text( parseInt(balance - 100 ))
				}else{
					console.log('err')
					$('#reactmessage').removeClass('hide')
					$('#reactmessage').text('An error occured!')
				}
				
			},
			error: function(err){
				console.log(err)
				$('#reactmessage').removeClass('hide')
				$('#reactmessage').text('An error occured!')
			}
		})
	})
})