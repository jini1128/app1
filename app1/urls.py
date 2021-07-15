from django.urls import path

from . import views

app_name='app1'

urlpatterns=[
    path('',views.index, name='index'),
#-------------------상세보기 페이지 추가 210712(태진)--------------------
    path('<int:question_id>/',views.detail, name='detail'),
    path('answer/create/<int:question_id>/',views.answer_create,name='answer_create'),
    #---------------210713 질문등록 url 부여------------------------
    path('question/create/',views.question_create, name='question_create')

]

