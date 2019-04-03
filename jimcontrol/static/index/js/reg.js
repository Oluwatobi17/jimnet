var usernames = []

$(document).ready(function(){

	$.ajax({
		url: '/api/usernames',
		method: 'get',
		success: function(data){
			for(var i=0; i<data.length; i++){
				usernames.push(data[i].username)
			}
		},
		error: function(err){
			console.log(err)
		}
	})
})


function checkusername(){
	var givename = $('input[name="username"]').val()
	if(usernames.indexOf(givename) == -1){
		return true;
	}else{
		$('#reactmessage').removeClass('hide')
		$('#reactmessage').text('Username: '+givename+' has been taken.')

		return false;
	}
}
function checksponsor(){
	var givename = $('input[name="sponsor"]').val()
	if(usernames.indexOf(givename) == -1){
		$('#reactmessage').removeClass('hide')
		$('#reactmessage').text('Sponsor: '+givename+' does not exit. Please check letter case.')
		
	}
}

function checkpassquality(){

	if($('input[name="password"]').val() != $('input[name="password2"]').val()){

		$('#reactmessage').removeClass('hide')
		$('#reactmessage').text('Passwords does not match')
	}
}

function checkpinquality(){
	console.log('Pin')
	if($('input[name="pincode"]').val() != $('input[name="pincode2"]').val()){
		console.log('Pincode mismath')	
		$('#reactmessage').removeClass('hide')
		$('#reactmessage').text('Pincodes does not match')
	}
}