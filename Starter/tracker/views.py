from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tracker.models import Transaction
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import json


User = get_user_model()
# Create your views here.

def index(request):
    return render(request, 'tracker/index.html')

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = authenticate(request, username=username, password=password)
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
def transactions_api_view(request, pk=None):
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
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            transactions = Transaction.objects.get(id = data['id'], user = request.user)
            transactions.date = data['date']
            transactions.type = data['type']
            transactions.amount = data['amount']
            transactions.save()
            return JsonResponse({'message':'Update completed successfully'})
        except Transaction.DoesNotExist:
            return JsonResponse ({'error': 'This transaction does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error':str(e)}, status=500)

    elif request.method == "DELETE":
        try:
            tx_id = pk  # from URL
            tx = Transaction.objects.get(id=tx_id, user=request.user)
            tx.delete()
            return JsonResponse({"message": "Deleted"})
        except Transaction.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)



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

@csrf_exempt
def signup_api_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': "POST Required"}, status=400)
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'error':'Missing Username or Password'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return JsonResponse({'message': 'User created successfully', 'user_id': user.id}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def transactions_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    context = {'transactions': transactions}
    return render(request, 'tracker/transactions-list.html', context)
