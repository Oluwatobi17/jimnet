from rest_framework import serializers
from index.models import User, Request
 

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username']



class ProcessingRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = Request
		fields = ['staffstatus', 'adminstatus']