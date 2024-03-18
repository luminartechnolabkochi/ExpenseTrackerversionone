from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets

from api.serializers import TransactionSerializer,TransactionSummarySerializer,RegistrationSerializer
from api.models import Transaction

from django.contrib.auth.models import User

from django.utils import timezone
from rest_framework.views import APIView
from django.db.models import Sum
from rest_framework import authentication,permissions


class TransactionView(viewsets.ModelViewSet):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=TransactionSerializer
    queryset=Transaction.objects.all()

    def get_queryset(self):
        return Transaction.objects.filter(user_object=self.request.user)

    def perform_create(self, serializer):
         return serializer.save(user_object=self.request.user)




class TransactionSummaryView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        cur_month=timezone.now().month
        cur_year=timezone.now().year
        transactions_qs=Transaction.objects.filter(
            created_date__month=cur_month,
            created_date__year=cur_year,
            user_object=request.user
            ) 
        
        total_income=transactions_qs.filter(type="income").values("amount").aggregate(total_income=Sum("amount"))
        total_expense=transactions_qs.filter(type="expenses").values("amount").aggregate(total_expense=Sum("amount"))
        category_summary=transactions_qs.values("category").annotate(total=Sum("amount"))
        summary=list(category_summary)

        
        # summary=[{dictionary.get("category"):dictionary.get("total")} for dictionary in category_summary]
        
       
        data={
            "total_income":total_income.get("total_income"),
            "total_expense":total_expense.get("total_expense"),
            "category_summary":summary
        }       

        return Response(data=data)
    


class SignUpView(APIView):

    def post(self,request,*args,**kwargs):

        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user_object=User.objects.create_user(**serializer.validated_data)
            serializer=RegistrationSerializer(user_object)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

    

