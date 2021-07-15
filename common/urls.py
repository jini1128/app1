from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

app_name = 'common'
# session : 일정시간동안 같은 사용자로부터 들어오는 요청을 하나의 상태로 보고 그 상태를 일정하게 유지시키는 기술.
#           사이트 방문자가 사이트에 접속해 있는 상태
# 일정시간 : 사이트에 접속한 시점부터 브라우저 종료까지
# 세션 특징 :
# 1. 웹 서버에 상태를 유지하기 위한 정보를 저장
# 2. 웹 서버에 저장되는 쿠키 - 세션쿠키
urlpatterns =[
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html') , name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]