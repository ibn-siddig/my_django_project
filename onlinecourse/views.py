from django.shortcuts import render, get_object_or_404
from .models import Course, Question, Choice, Submission
from django.http import HttpResponseRedirect
from django.urls import reverse


# عرض تفاصيل الكورس والدروس
def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_detail_bootstrap.html', {'course': course})


# دالة submit لمعالجة إجابات الطالب وعرض النتيجة مباشرة
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        # جمع اختيارات الطالب
        selected_ids = request.POST.getlist('choice')
        total_score = 0

        # جلب كل الأسئلة المرتبطة بالكورس
        questions = Question.objects.filter(course=course)
        max_score = questions.count()

        for question in questions:
            correct_choices = question.choice_set.filter(is_correct=True)
            user_choices_for_q = [
                int(id) for id in selected_ids
                if int(id) in question.choice_set.values_list('id', flat=True)
            ]

            # إذا تطابقت اختيارات الطالب مع الصحيحة تماماً
            if user_choices_for_q and set(user_choices_for_q) == set(correct_choices.values_list('id', flat=True)):
                total_score += 1

        # إرسال النتيجة لنفس صفحة التفاصيل لعرض رسالة التهنئة
        context = {
            'course': course,
            'grade': total_score,
            'total_score': max_score
        }

        return render(request, 'onlinecourse/course_detail_bootstrap.html', context)

    return HttpResponseRedirect(reverse('onlinecourse:course_details', args=(course.id,)))


# دالة show_exam_result لعرض النتيجة التفصيلية بعد حفظ الاختيارات
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    # حساب الدرجة التفصيلية
    total_score = 0
    questions = Question.objects.filter(course=course)

    for question in questions:
        correct_choices = question.choice_set.filter(is_correct=True)
        user_choices_for_q = submission.choices.filter(question=question)

        if set(user_choices_for_q) == set(correct_choices):
            total_score += 1

    context = {
        'course': course,
        'submission': submission,
        'grade': total_score,
        'total_score': questions.count()
    }

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)