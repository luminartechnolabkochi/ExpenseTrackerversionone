from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets

from api.serializers import TransactionSerializer,TransactionSummarySerializer
from api.models import Transaction

from django.utils import timezone
from rest_framework.views import APIView
from django.db.models import Sum


class TransactionView(viewsets.ModelViewSet):
    serializer_class=TransactionSerializer
    queryset=Transaction.objects.all()



class TransactionSummaryView(APIView):

    def get(self,request,*args,**kwargs):
        cur_month=timezone.now().month
        cur_year=timezone.now().year
        transactions_qs=Transaction.objects.filter(
            created_date__month=cur_month,
            created_date__year=cur_year
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
    


