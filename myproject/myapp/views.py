from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView,TemplateView
from django.http import HttpResponse, Http404,JsonResponse, HttpResponseNotAllowed
from django.core.serializers import serialize
from django.forms import formset_factory
from django.utils.dateparse import parse_datetime
from pytz import timezone
from datetime import datetime, timedelta
import calendar
from .models import Developer, Building, Apartment, Buyer, Contract, UserProfile, Order, Land, Event, Report
from .forms import OrderDetailForm, BuildingForm, UserRegisterForm, OrderForm, LandForm, OrderDetailForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# %%%%%%%%%%%%%%%%%%%homepageview%%%%%%%%%%%%%%%%%%%%%%%%%
def home_view(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-order_date')
    else:
        orders = None
    return render(request, 'homepage.html', {'orders': orders})


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%Developer CLUD%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
@login_required
def developer_list(request):
    developers = Developer.objects.all()
    return render(request, 'developer_list.html', {'developers': developers})






class BuildingDetailView(DetailView):
    model = Building
    template_name = 'building_detail.html'
    context_object_name = 'building'


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# register ID
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # User 모델 인스턴스 저장

            # UserProfile 모델 인스턴스 생성 및 저장
            profile = UserProfile(user=user, name=form.cleaned_data['name'],
                                  company_name=form.cleaned_data['company_name'],
                                  phone_number=form.cleaned_data['phone_number'],
                                  address=form.cleaned_data['address'],
                                  fax_number=form.cleaned_data['fax_number'],
                                  housenumber=form.cleaned_data['housenumber'],
                                  email=form.cleaned_data['email'],
                                  name_leader=form.cleaned_data['name_leader'],
                                  department=form.cleaned_data['department'],
                                  company_number=form.cleaned_data['company_number'],
                                  housing_license=form.cleaned_data['housing_license'],
                                  )
            profile.save()

            # 성공 메시지 표시
            messages.success(request, 'アカウントが成功的に生成できました!')

            # 사용자를 로그인 페이지나 홈페이지로 리디렉션
            return redirect('login')  # 'login'은 해당 페이지의 URL 패턴 이름

    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

# 필요에 따라 LoginView를 커스텀할 수 있습니다
class CustomLoginView(LoginView):
    template_name = 'login.html'
    # 추가 설정(예: 리디렉션, 폼 클래스 지정 등)

def my_view(request):
    if request.user.is_authenticated:
        # 로그인한 사용자의 경우
        # 로그인한 사용자에 대한 처리
        context = {'message': 'ログインした使用者です.'}
        return render(request, 'homepage.html', context)
    else:
        # 로그인하지 않은 사용자의 경우
        # 로그인하지 않은 사용자에 대한 처리
        return redirect('login')  # 로그인 페이지로 리디렉션

    # return render(request, 'homepage.html')
# 発注フォーム
@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            # 정확한 데이터가 저장되었는지 확인
            print("Saved quantities:", order.land_quantity, order.building_quantity)
            # building_order_view 함수로 리다이렉트
            return redirect('building_order_view', order_id=order.id, land_quantity=order.land_quantity, building_quantity=order.building_quantity)
        else:
            print("Failed:", form.errors)
    else:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            form = OrderForm(initial={
                'name': user_profile.name,
                'company_name': user_profile.company_name
            })
        except UserProfile.DoesNotExist:
            form = OrderForm()

    return render(request, 'order_form.html', {'form': form})



def building_order_view(request, order_id, land_quantity, building_quantity):
    order = get_object_or_404(Order, pk=order_id)
    LandFormSet = formset_factory(LandForm, extra=land_quantity)
    BuildingFormSet = formset_factory(BuildingForm, extra=building_quantity)

    if request.method == 'POST':
        form = OrderDetailForm(request.POST, request.FILES, instance=order)
        land_formset = LandFormSet(request.POST, prefix='land')
        building_formset = BuildingFormSet(request.POST, prefix='building')
        if form.is_valid() and land_formset.is_valid() and building_formset.is_valid():
            form.save()
            for land_form in land_formset:
                land = land_form.save(commit=False)
                land.order = order
                land.save()
            for building_form in building_formset:
                building = building_form.save(commit=False)
                building.order = order
                building.save()
            # 성공 메시지 추가
            messages.success(request, '주문이 성공적으로 처리되었습니다.')
            return redirect('home')  # 'home'은 홈페이지의 URL 이름입니다.
    else:
        # GET 요청 시 폼셋 초기화
        form = OrderDetailForm(instance=order)
        land_formset = LandFormSet(prefix='land')
        building_formset = BuildingFormSet(prefix='building')

    context = {
        'form': form,
        'land_forms': land_formset,
        'building_forms': building_formset,
    }
    return render(request, 'building_order_form.html', context)

    # if request.method == 'POST':
    #     building_form = BuildingForm(request.POST)
    #     land_form = LandForm(request.POST)
    #     if building_form.is_valid() and land_form.is_valid():
    #         building_form.save()
    #         land_form.save()
    #         messages.success(request, '주문이 성공적으로 처리되었습니다.')
    #         return redirect('home')
    #     else:
    #         messages.error(request, '오류가 발생했습니다. 입력 정보를 확인해 주세요.')
    # else:
    #     building_form = BuildingForm()
    #     land_form = LandForm()

    # return render(request, 'building_order_form.html', {'building_form': building_form, 'land_form': land_form})
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        form = OrderDetailForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            return redirect('some_success_url')  
    else:
        form = OrderDetailForm(instance=order)
    
    return render(request, 'building_order_form.html', {'form': form})

def order_history(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-order_date')
        return {'order_history': orders}
    return {}

def view_schedule(request):
    orders = Order.objects.filter(user=request.user).order_by('order_date')
    return render(request, 'view_schedule.html', {'orders': orders})

def order_events(request):
    orders = Order.objects.filter(user=request.user)
    events = [
        {
            'title': f'注文 #{order.id}',
            'start': order.order_date,
            'end': order.expected_contract_date
        } for order in orders
    ]
    return JsonResponse(events, safe=False)

# password
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('change_password_done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def calendar_view(request):
    all_events = Event.objects.all()
    print(all_events)
    context = {
        "event": all_events,
    }
    print(context)
    return render(request, 'calendar.html', context)

def all_events(request):
    all_events = Event.objects.all()
    print(all_events)
    out = []
    for event in all_events:
        out.append({
            'title': event.title,
            'id' : event.id,
            'start' : event.start_date.strftime("%m/%d/%Y, %H:%M:%S"),
            'end' : event.end_date.strftime("%m/%d/%Y, %H:%M:%S"),
        })

    return JsonResponse(out, safe=False)
@login_required
def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Event(title=str(title), start_date=start, end_date=end, user=request.user)
    event.save()
    print(f"Added event: {event.title}, Start: {event.start_date}, End: {event.end_date}")

    data = {"status": "success", "message": "Event added successfully"}
    return JsonResponse(data)
@login_required
def update(request):
    start = request.GET.get("start",None)
    end = request.GET.get("end",None)
    title = request.GET.get("title",None)
    id = request.GET.get("id",None)
    event= Event.objects.get(id=id, user=request.user)
    event.start_date = start
    event.end_date = end
    event.title = title
    event.save()
    data = {}
    return JsonResponse(data)

@login_required
def remove(request):
    id = request.GET.get("id", None)
    event = Event.objects.get(id=id,user=request.user)
    event.delete()
    data = {}
    return JsonResponse(data)

@login_required
def all_events(request):
    events = Event.objects.filter(user=request.user)  # 현재 사용자의 이벤트만 필터링
    event_list = []
    for event in events:
        event_list.append({
            'id': event.id,
            'title': event.title,
            'start': event.start_date.strftime("%Y-%m-%dT%H:%M:%S"),
            'end': event.end_date.strftime("%Y-%m-%dT%H:%M:%S"),
        })
    return JsonResponse(event_list, safe=False)
    
def dashboard_view(request):
    reports = Report.objects.all()
    return render(request, 'dashboard.html', {'reports': reports})




