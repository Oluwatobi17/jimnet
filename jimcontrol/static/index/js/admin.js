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
	$('.deletebut').on('click', function(){
		var id = $(this).data('pk')
		$.ajax({
			url: '/jimcontrol/admin/deletepin/'+id,
			method: 'get',
			success: function(data){
				console.log('Deletion successful!')
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
})