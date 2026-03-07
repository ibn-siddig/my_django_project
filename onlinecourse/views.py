from django.shortcuts import render, get_object_or_404
from .models import Course, Question, Choice
from django.http import HttpResponseRedirect
from django.urls import reverse

# دالة عرض تفاصيل الكورس (تأكد من وجودها للسؤال 4 و 5)
def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_detail_bootstrap.html', {'course': course})

# دالة الـ submit المطلوبة في السؤال الرابع (حساب النتيجة)
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        # الحصول على قائمة معرفات الخيارات التي اختارها الطالب
        selected_ids = request.POST.getlist('choice')
        total_score = 0
        
        # جلب كل الأسئلة المرتبطة بهذا الكورس
        questions = Question.objects.filter(course=course)
        for question in questions:
            # جلب الخيارات الصحيحة لهذا السؤال فقط
            correct_choices = question.choice_set.filter(is_correct=True)
            # جلب اختيارات الطالب التي تنتمي لهذا السؤال
            user_choices_for_q = [int(id) for id in selected_ids if int(id) in question.choice_set.values_list('id', flat=True)]
            
            # إذا تطابقت اختيارات الطالب تماماً مع الاختيارات الصحيحة
            if set(user_choices_for_q) == set(correct_choices.values_list('id', flat=True)):
                total_score += 1
                
        # إرسال النتيجة النهائية لصفحة النتائج
        return render(request, 'onlinecourse/exam_result.html', {'course': course, 'score': total_score})