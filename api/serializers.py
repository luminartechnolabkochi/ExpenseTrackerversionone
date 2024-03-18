from rest_framework import serializers
from api.models import Transaction
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=["username","email","password"]
        



class TransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Transaction
        fields="__all__"
        read_only_fields=["id","created_date"]


# {"total_expense":1245,"total_income":4567,
#         "categroy_summary":
#         [
#         {"category":"food",total_amount:345},
#         
#         ]
# }

class TransactionSummarySerializer(serializers.Serializer):
    total_expense=serializers.DecimalField(max_digits=10,decimal_places=2)
    total_income=serializers.DecimalField(max_digits=10,decimal_places=2)
    category_summary=serializers.DictField(child=serializers.DecimalField(max_digits=10,decimal_places=2))
        
