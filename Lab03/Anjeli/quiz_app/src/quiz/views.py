from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.db import transaction
from .models import Exam, Question, Choice
from .forms import ExamForm, QuestionForm, ChoiceFormSet

def exam_list(request):
    """Vista para listar todos los exámenes"""
    exams = Exam.objects.all().order_by('-created_date')
    return render(request, 'quiz/exam_list.html', {'exams': exams})

def exam_detail(request, exam_id):
    """Vista para mostrar el detalle de un examen con sus preguntas"""
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all().prefetch_related('choices')
    return render(request, 'quiz/exam_detail.html', {'exam': exam, 'questions': questions})

def exam_create(request):
    """Vista para crear un nuevo examen"""
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save()
            messages.success(request, 'Examen creado correctamente.')
            return redirect('question_create', exam_id=exam.id)
    else:
        form = ExamForm()
    
    return render(request, 'quiz/exam_form.html', {'form': form})

def question_create(request, exam_id):
    """Vista para añadir preguntas a un examen"""
    exam = get_object_or_404(Exam, id=exam_id)
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        
        if question_form.is_valid():
            with transaction.atomic():
                # Guardar la pregunta
                question = question_form.save(commit=False)
                question.exam = exam
                question.save()
                
                # Procesar el formset para las opciones
                formset = ChoiceFormSet(request.POST, instance=question)
                if formset.is_valid():
                    formset.save()
                    
                    # Verificar que solo una opción sea marcada como correcta
                    correct_count = question.choices.filter(is_correct=True).count()
                    if correct_count != 1:
                        messages.warning(request, 'Debe haber exactamente una respuesta correcta.')
                    else:
                        messages.success(request, 'Pregunta añadida correctamente.')
                        
                    # Decidir a dónde redirigir
                    if 'add_another' in request.POST:
                        return redirect('question_create', exam_id=exam.id)
                    else:
                        return redirect('exam_detail', exam_id=exam.id)
    else:
        question_form = QuestionForm()
        formset = ChoiceFormSet()
    
    return render(request, 'quiz/question_form.html', {
        'exam': exam,
        'question_form': question_form,
        'formset': formset,
    })
def exam_update(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, 'Examen actualizado correctamente.')
            return redirect('exam_detail', exam_id=exam.id)
    else:
        form = ExamForm(instance=exam)
    return render(request, 'quiz/exam_form.html', {'form': form})


def exam_delete(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        exam.delete()
        messages.success(request, 'Examen eliminado correctamente.')
        return redirect('exam_list')
    return render(request, 'quiz/exam_confirm_delete.html', {'exam': exam})


def exam_play(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.prefetch_related('choices')
    
    if request.method == 'POST':
        correct = 0
        total = questions.count()
        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected and question.choices.filter(id=selected, is_correct=True).exists():
                correct += 1
        return render(request, 'quiz/exam_result.html', {
            'exam': exam,
            'correct': correct,
            'total': total
        })
    
    return render(request, 'quiz/exam_play.html', {'exam': exam, 'questions': questions})
def question_update(request, exam_id, question_id):
    exam = get_object_or_404(Exam, id=exam_id)
    question = get_object_or_404(Question, id=question_id)

    # Limitar el formset a 4 opciones máximo
    ChoiceFormSetLimited = inlineformset_factory(
        Question,
        Choice,
        formset=ChoiceFormSet,
        fields=['text', 'is_correct'],  # Especificar los campos que se mostrarán
        extra=max(0, 4 - question.choices.count()),  # Ajuste dinámico
        max_num=4,  # Máximo de 4 opciones
        can_delete=True
    )

    if request.method == 'POST':
        question_form = QuestionForm(request.POST, instance=question)
        formset = ChoiceFormSetLimited(request.POST, instance=question)

        if question_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                question_form.save()
                formset.save()

                # Validar que solo haya una respuesta correcta
                correct_count = question.choices.filter(is_correct=True).count()
                if correct_count != 1:
                    messages.warning(request, 'Debe haber exactamente una respuesta correcta.')
                else:
                    messages.success(request, 'Pregunta actualizada correctamente.')

                if 'add_another' in request.POST:
                    return redirect('question_create', exam_id=exam.id)
                else:
                    return redirect('exam_detail', exam_id=exam.id)
    else:
        question_form = QuestionForm(instance=question)
        formset = ChoiceFormSetLimited(instance=question)

    return render(request, 'quiz/question_form.html', {
        'exam': exam,
        'question_form': question_form,
        'formset': formset,
        'espaciado': 'p-3 mb-4 rounded shadow-sm',  # 👈 esto lo usaremos en el template
    })
