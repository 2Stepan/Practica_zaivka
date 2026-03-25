from django.shortcuts import render, redirect, get_object_or_404
from .models import Request
# Create your views here.

 
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

def get(request):
    request_item = None
    request_item_id = request.GET.get('request_item_id')

    if request_item_id:
        try:
            request_item = Request.objects.get(id=request_item_id)
        except Request.DoesNotExist:
            request_item = None  # или любое другое действие

    return render(request, 'request_get/index.html', {
        'request_item': request_item,
        'request_item_id': request_item_id,
    })