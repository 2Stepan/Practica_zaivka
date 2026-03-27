from django.shortcuts import render, redirect, get_object_or_404
from .models import Request, users
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
# Create your views here.

#Артем
def show(request):

    context = {}

    if 'user_id' in request.session:
        try:
            user = users.objects.get(id=request.session['user_id'])
            context['user'] = user
            context['is_authenticated'] = True
        except users.DoesNotExist:
            request.session.flush()
            context['is_authenticated'] = False
    else:
        context['is_authenticated'] = False
    return render(request, 'main/index.html')

def reg(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')  # Получаем выбранную роль

        if users.objects.filter(email=email).exists():
            print("Такой пользователь уже существует!")
            data = {"header": "Такой пользователь существует", "message": "Попробуйте снова!"}
            return render(request, "register/index.html", context=data)

        hashed_password = make_password(password)

        users.objects.create(
            email=email,
            password=hashed_password,
            role=role  # Сохраняем выбранную роль
        )

        data = {"header": email, "message": "Добро пожаловать!"}
        return render(request, "main/index.html", context=data)

    return render(request, 'register/index.html')


from django.contrib.auth.hashers import check_password

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Пользователь с указанным email
        user = users.objects.filter(email=email).first()

        # Проверяем, существует ли пользователь и совпадает ли пароль
        if user and check_password(password, user.password):

            request.session['user_id'] = user.id
            request.session['user_email'] = user.email
            request.session['user_role'] = user.role
            print("{ user.email } вы вошли в аккаунт, Поздравляем!")

            data = {"header": email, "message": "Добро пожаловать!"}
            return render(request, 'main/index.html', context=data)
        else:
            print("Нет аккаунта!")
            data = {"header": "Неправильный пароль", "message": "Попробуйте снова!"}
            return render(request, 'auth/index.html', context=data)

    print("Страница отрендерилась!")
    return render(request, 'auth/index.html')

def logout(request):

    request.session.flush()

    return redirect('show')




def add(request): 
    if 'user_id' not in request.session:
        
        return redirect('login')
    
    if request.method == 'POST':
        # Получаем данные из формы
        user = users.objects.get(id=request.session['user_id'])
        client_name = request.POST.get('client_name')
        contacts = request.POST.get('contacts')
        service = request.POST.get('service')
        description = request.POST.get('description')
        status = request.POST.get('status')

        # Создаём новую заявку
        Request.objects.create(
            client_name=client_name,
            client_email=user.email,
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