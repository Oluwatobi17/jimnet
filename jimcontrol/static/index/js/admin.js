$(document).ready(function(){
		// Handling admin process button process
	$('.processbut').on('click', function(){
		var id = $(this).data('pk')
		$.ajax({
			url: '/jimcontrol/admin/processrequest/'+id,
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

	// Handling admin delete pin button
	$('table .deletebut').on('click', function(){
		var id = $(this).data('pk')
		$.ajax({
			url: '/jimcontrol/admin/deletepin/'+id,
			method: 'get',
			success: function(data){
				$('#'+id).removeClass('active').removeClass('deletebut')
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

	$('#create .newst').on('click', function(){
		$('#create #newstaff').removeClass('hide')
		$('#create #newagent').addClass('hide')
	})

	$('#create .newag').on('click', function(){
		$('#create #newagent').removeClass('hide')
		$('#create #newstaff').addClass('hide')
	})

	$('#agent .delagent').on('click', function(){
		var self = $(this)
		$.ajax({
			url: '/jimcontrol/admin/deleteagent/' + $(this).data('agent'),

			success: function(data){
				if(data){
					self.closest('.infodrop').remove()
				}else{
					console.log(err)
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

	

	// agent
	$('#agent .more').on('click', function(){
		var agentId = $(this).data('drop').replace('agent', '')
		var self = $(this)
		$.ajax({
			url: '/api/getAgentBookings/' + agentId,
			method: 'get',
			success: function(data){

				if(data.length!=0){
					$('#temp'+agentId).closest('.bookusersTemplateClass').html('')
					var template = $('#bookusersTemplate').html();
					for(var i=0;i<data.length;i++){
						$('#temp'+agentId).closest('.bookusersTemplateClass').append(Mustache.render(template, data[i]))
					}
					
				}else{
					info = "<h6>No info found</h6>"
					$('#temp'+agentId).closest('.bookusersTemplateClass').html(info)
				}
				
			},
			error: function(err){
				console.log(err)
				$('#reactmessage').removeClass('hide')
				$('#reactmessage').text('An error occured!')
			}
		})
	})

	$('#booked .deletebut').on('click', function(){
		var id = $(this).attr('id')

		$.ajax({
			url: '/jimcontrol/admin/deletebooking/' + id.replace('delete', ''),
			success: function(data){
				if(data){
					$('#booked #'+id).closest('.infodrop').remove()
				}else{
					console.log(err)
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


	$('#agent .updateAgentBalance').on('submit', function(){
		var id = $(this).data('agent')
		var self = $(this)
		var newbal = $('#'+id+'balText').val()
		if (newbal%100 != 0){
			alert('Please the amount must be a multiple of 100')
			return;
		}

		$(this).off('submit')
		$.ajax({
			method: 'POST',
			url: '/jimcontrol/admin/updateagentbalance/' + id +'/',
			data: {
				'balance': newbal,
				'csrfmiddlewaretoken': self.closest('.balToken').text()
			},
			success: function(data){
				if(data){
					$('#balance'+id).text( parseInt($('#balance'+id).text())+ parseInt(newbal))
					$('#'+id+'balText').val('')
				}else{
					console.log(err)
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

	$('#members .infodrop .paymemberbyhand').on('submit', function(){
		var id = $(this).data('member')
		var self = $(this)
		var oldbal = parseInt($('#members .infodrop #'+id+'membalance').text())
		var amount = parseInt($('#'+id+'amount').val())
		if (amount>oldbal){
			alert('Insuficient fund.')
			return;
		}

		$(this).off('submit')
		$.ajax({
			method: 'POST',
			url: '/jimcontrol/admin/paymemberbyhand/' + id +'/',
			data: {
				'amount': amount,
				'csrfmiddlewaretoken': self.closest('.balToken').text()
			},
			success: function(data){
				if(data){
					$('#members .infodrop #'+id+'membalance').text(oldbal-amount)
					$('#'+id+'amount').val('')
				}else{
					console.log(err)
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