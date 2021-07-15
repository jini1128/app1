from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
# views.py의 위치에서 models.py를 찾아서 qusetion을 import하라는 의미
from .models import Question,Answer
from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from app1.forms import QuestionForm,AnswerForm
# 210719 페이징처리 관련 모듈 import
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    # request : 외부 사용자의 요청을 받아오는것
    # render : 템플릿을 로딩할 때 사용
    # redirect : URL로 이동시 사용
    # 사용자가 localhost:8000/app1 페이지 접속이라는 요청을 보냈다.
    # view -> urls에 어떤 함수를 실행해야 하는지를 확인
    #210709 질문 목록 가져오기
    # view에서 model단에 요청
    # 요청의 내용 : 조회 (Question 테이블/모델 create_date컬럼을 기준으로
    #               정렬해서 가져옴) -> 그 결과를 question_list 변수에 저장

    page=request.GET.get('page','1')

    question_list = Question.objects.order_by('-create_date')
    # context라는 변수에 딕셔너리 형태로 question_list key와 value를 저장
    # 템플릿단에서 해당 데이터를 쉽게 조회하기 위해
    # 페이징 처리 내용
    # 가져온 데이터를 10개씩 보여줘라~
    paginator=Paginator(question_list,10)
    page_obj=paginator.get_page(page)

    context = {'question_list':page_obj}
    # 받은 요청에 대해(request)
    # app1/question.list.html 템플릿을 열어주고
    # 해당 템플릿에 context 변수의 값을 전송
    return render(request,'app1/question_list.html',context)

def detail(request,question_id):
    # get_object_or_404 : 기본키에 해당하는 건이 없다면 404페이지 출력
    question = get_object_or_404(Question, pk=question_id)
    context = {'question' : question}
    return render(request, 'app1/question_detail.html', context)

# 수정전 answer_create 코드 210723 백업
# def answer_create(request,question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     question.answer_set.create(answer_content=request.POST.get('answer_content'),create_date=timezone.now())


    # return redirect('app1:detail',question_id=question.id)

    #210723 answer_create 수정  TJKim
    # 기존 answer_create 기능 중 로그인 하지 않은 사용자도 답변을 달수 있다라는 문제점이 발견되어 수정.
    # author컬럼이 추가됨에 따라 답변 작성자를 저장하기 위한 코드 수정.
@login_required(login_url='common:login')
def answer_create(request,question_id):

    question=get_object_or_404(Question, pk=question_id)
    #답변 수정은 답변 작성자만 수정 가능하게끔 처리하는 코드
    #답변 작성자와 로그인한 유저가 같은지 확인

    if request.method=="POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer=form.save(commit=False)
            answer.create_date=timezone.now()
            answer.author=request.user
            answer.question=question
            answer.save()
            return redirect('app1:detail',question_id=question.id)
    else:
        form=AnswerForm()
    context={'question':question,'form':form}
    return render(request,'app1/question_detail.html',context)


# 질문등록 함수 210713
# login_required 데코레이터를 추가함으로써
# 만약 질문등록하기 페이지 이동시 로그인이 안되어 있다면
# 로그인페이지로 먼저 이동시킨다
@login_required(login_url='common:login')
def question_create(request):
    #수정 내용 : GET,POST방식에 대한 처리
    #question_form으로 들어올때
    #질문을 등록할 때
    # POST방식인지 GET방식인지 확인
    # 이유 : 단순히 질문등록 페이지를 오픈한 것인지
    # 아니면 질문 등록페이지에 데이터를 입력해 저장한것인지를 구분.
    if request.method == 'POST':
        # forms.py에 설정한 QuestionForm 클래스를 호출
        # request.POST : 사용자가 입력한 데이터를 받아온다.
        form = QuestionForm(request.POST)
        # 변수 form에 들어온 값이 올바른 값(정상적인값)인지를 확인.
        if form.is_valid():
            # 저장을 하기전 잠시 유보.
            # question변수에 form에서 받아온 데이터는 넣어뒀지만
            # 아직 DB로 저장하지는 않았다!
            question = form.save(commit=False)
            # create_date 컬럼을 따로 입력받지 않은 이유?
            # 질문등록의 날짜 시간의 경우 현재 시간으로 입력받기 위해
            # view에서 처리
            question.create_date=timezone.now()
            question.author=request.user
            question.save()
            return redirect('app1:index')
    else:
        form=QuestionForm()
    context={'form':form}

    return render(request,'app1/question_form.html',context)

#210721 질문수정 기능
@login_required(login_url='common:login')
def question_modify(request,question_id):

    question=get_object_or_404(Question, pk=question_id)

    # 본인이 쓴글은 본인만 수정 가능하게
    if request.user!=question.author:
        messages.error(request,"수정권한이 없읍니다")
        return redirect('app1:detail',question_id=question_id)

    #전송방식이 POST인지 확인(question_form으로 접속만 한건지 아니면 데이터를 전송받아 왔는지 체크)
    if request.method=="POST":
        #instance = question
        #인스턴스 파라미터에 question 테이블을 지정해 기존의 값을 form에 채워 넣음.
        #만약 전달받은 데이터가 있다면 전달받은 입력값을 덮어써서 QuestionForm을 재 생성.
        form = QuestionForm(request.POST,instance=question)
        if form.is_valid():
            question=form.save(commit=False)
            question.author=request.user
            question.modify_date=timezone.now()
            question.save()
            #수정된 내용 저장을 완료 후 question_detail페이지로 이동
            #주의사항 : 일반적인 방식으로 redirect한다면 key값(id값)을 찾을 수 가 없다.
            #         그러한 상황을 방지하기 위해 question_id에 기존 컬럼의 key값을 return
            return redirect('app1:detail',question_id=question_id)

    form=QuestionForm(instance=question)
    return render(request,'app1/question_form.html',{'form':form})

# 210722 질문 삭제 함수 등록
@login_required(login_url='common:login')
def question_delete(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    if request.user != question.author:
        messages.error(request, "삭제권한이 없읍니다")
        return redirect('app1:detail',question_id=question_id)
    question.delete()
    return redirect('app1:index')

# 210723 답변 수정 함수 등록

@login_required(login_url='common:login')
def answer_modify(request,answer_id):

    answer=get_object_or_404(Answer,pk=answer_id)
    #답변 수정은 답변 작성자만 수정 가능하게끔 처리하는 코드
    #답변 작성자와 로그인한 유저가 같은지 확인 
    if request.user!=answer.author:
        # 다르다면 에러메세지를 템플렛단에 전송
        messages.error(request,'수정권한이 없읍니다')
        return redirect('app1:detail',question_id=answer.question.id)

    if request.method=="POST":
        form = AnswerForm(request.POST,instance=answer)
        if form.is_valid():
            answer=form.save(commit=False)
            answer.author=request.user
            answer.modify_date=timezone.now()
            answer.save()
            return redirect('app1:detail',question_id=answer.question.id)
    else:
        form=AnswerForm()
    context={'form':form}
    return render(request,'app1/answer_form.html',context)


# 210723 답변 삭제 함수
@login_required(login_url='common:login')
def answer_delete(request,answer_id):
    answer=get_object_or_404(Answer,pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "삭제권한이 없읍니다")
        return redirect('app1:detail',answer_id=answer_id)
    answer.delete()
    return redirect('app1:detail',question_id=answer.question.id)



#0714수정 (기존내용 백업)
# def question_create(request):
#     form = QuestionForm()
#     return render(request, 'app1/question_form.html', {'form': form})


# get방식 post방식(데이터 전송 방식)
# get방식 : url에 파라미터를 붙여서 전송하는 방식
#         속도가 빠르다는 장점이 있지만
#         url에 데이터를 실어서 보내기 때문에 보안에 취약하거나
#         그 외 데이터 전송에 여러가지 제한사항이 있다
# post방식 : html의 body영역에 데이터를 실어 보내는 방식(form태그)
#           대용량의 데이터를 보낼 수 있고 주소에 실어 보내지 않기 때문에 get방식에 비해 보안성 또한 좋다

#CSRF_TOKEN: 브라우저에서 작성된 데이터가 올바른 데이터인지,
#            혹은 진짜 웹 브라우저에서 작성된 데이터인지 판단하는 기능

# <!--템플릿 태그-->
# <!--{% if 요청 받은 값(question_list) %} : question_list가 있을경우-->
# <!--{% for 임시변수 in 요청받은값(딕셔너리 키값) %} : 딕셔너리의 키의 value를-->
# <!--반복하여 순차적으로 임시변수에 대입-->
# <!--{{ 임시변수.컬럼 }} : for문에 의해 선언된 임시변수의 컬럼출력-->

def test(request):
    return render(request,'app1/template2.html')