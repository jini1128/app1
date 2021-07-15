from django import forms
from app1.models import Question

# QuestionForm 같은 클래스를 장고 폼이라 부른다
# 장고 폼 에는 2가지 폼이 있고
# 일반 폼, 모델 폼 이라는것이 있음
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject','content']

#-------210714질문 등록하기 제목, 내용에 부트스트랩 적용---------------
# 왜 html에서 적용하지 않고 모듈에서 적용하는가?
#이유 : 템플릿태그 {{form.as_p}} 때문
#{{form.as_p}}: 모델(테이블)의 정보를 받아 form과 요소를 자동으로 생성하는 템플릿 태그
#테이블 컬럼 숫자에 관계없이 컬럼을 불러올 수 있다는 장점이 있지만
# html(템플릿)단 에서 스타일을 적용하기 힘들다 라는 단점이 있음
# 이러한 단점을 widget속성을 이용해서 해당 템플릿(html)로딩시 클래스 정보를 전달해주는 방식으로 커버한다.
#key값은 해당 컬럼명으로 value값은 적용할 속성으로 쓴다.

        widgets={
            'subject': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control','rows':10}),
        }
        
        labels={
            'subject':'제목',
            'content':'질문내용',
        }