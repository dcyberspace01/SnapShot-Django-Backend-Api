from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tracker.models import Transaction
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json



# Create your views here.

def index(request):
    return render(request, 'tracker/index.html')

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("username")
            password = data.get("password")

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"message": "Login successful"})
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Only POST allowed"}, status=405)

@csrf_exempt
@login_required
def transactions_api_view(request):
    if request.method == "GET":
        transactions = Transaction.objects.filter(user=request.user)
        data = [
            {"id": t.id, "date": t.date, "type": t.type, "amount": t.amount}
            for t in transactions
        ]
        return JsonResponse(data, safe=False)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            Transaction.objects.create(
                user=request.user,
                date=data["date"],
                type=data["type"],
                amount=data["amount"]
            )
            return JsonResponse({"message": "Transaction added"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@login_required
def user_api_view(request):
    try:
        return JsonResponse({"username": request.user.username})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"message": "Logged out"})
    return JsonResponse({"error": "Only POST allowed"}, status=405)

@login_required
def transactions_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    context = {'transactions': transactions}
    return render(request, 'tracker/transactions-list.html', context)
