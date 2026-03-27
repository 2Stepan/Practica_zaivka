from django.shortcuts import render, redirect, get_object_or_404
from .models import Request
# Create your views here.

#Артем
def show(request):
    return render(request, 'main/index.html')

def add(request): 
    if request.method == 'POST':
        # Получаем данные из формы
        client_name = request.POST.get('client_name')
        contacts = request.POST.get('contacts')
        service = request.POST.get('service')
        description = request.POST.get('description')
        status = request.POST.get('status')

        # Создаём новую заявку
        Request.objects.create(
            client_name=client_name,
            contacts=contacts,
            service=service,
            description=description,
            status=status
        )

        # Перенаправляем пользователя на страницу успеха
        return render(request, 'success/index.html', {'message': 'Заявка успешно создана!'})

    # Если метод не POST, просто отображаем форму
    return render(request, 'create/index.html') 


def view_requests(request):
    # Получаем все заявки из базы данных
    requests_list = Request.objects.all()
    # Передаем список заявок в шаблон
    return render(request, 'requests/index.html', {'requests': requests_list})


#Егор
def update(request, request_id):
    request_object = get_object_or_404(Request, id = request_id)

    if request.method == 'POST':
        service = request.POST.get('service')
        description = request.POST.get('description')
        status = request.POST.get('status')


        request_object.service = service
        request_object.description = description
        request_object.status = status

        request_object.save()

        return redirect('view_requests')
    
    return render (request, 'update/index.html', {'request': request_object})

def delete(request, request_id):
    request_object = get_object_or_404(Request, id=request_id)

    request_object.delete()

    return redirect('view_requests')
    




# Ваня - исправил поиск, теперь показывает сообщение если нет заявки
def get(request):


    query = request.GET.get("q")

    requests = Request.objects.all()

    if query:
        from django.db.models import Q

        requests = Request.objects.filter(
            Q(id__icontains=query) |
            Q(client_name__icontains=query) |
            Q(service__icontains=query)
        )

    return render(
        request,
        "partials/request_rows.html",
        {"requests": requests}
    )