from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Candidate, Question, Option, Result, Report

# Base Page (Login)
def base(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('code')
        try:
            candidate = Candidate.objects.get(email=email, unique_code=code)
            request.session['candidate_id'] = candidate.id
            return redirect('home')
        except Candidate.DoesNotExist:
            messages.error(request, 'Invalid email or code')
    return render(request, 'quiz/base.html')

# Home Page
def home(request):
    candidate_id = request.session.get('candidate_id')
    if not candidate_id:
        return redirect('base')
    candidate = Candidate.objects.get(id=candidate_id)
    return render(request, 'quiz/home.html', {'candidate': candidate})

# Quiz Page
def quiz(request):
    candidate_id = request.session.get('candidate_id')
    if not candidate_id:
        return redirect('base')
    candidate = Candidate.objects.get(id=candidate_id)
    questions = Question.objects.all()

    if request.method == 'POST':
        total_marks = 0
        for question in questions:
            selected_option = request.POST.get(str(question.id))
            if selected_option:
                option = Option.objects.get(id=selected_option)
                total_marks += option.marks
        
        # Calculate percentage safely
        max_marks = sum(q.marks for q in questions)
        if max_marks > 0:
            percentage = (total_marks / max_marks) * 100
        else:
            messages.error(request, "Quiz is not configured correctly (max marks = 0).")
            return redirect('home')

        # Determine suggestions based on percentage
        if percentage < 30:
            suggestion = "Keep practicing! You can do better."
        elif 30 <= percentage < 70:
            suggestion = "Good job, but there's room for improvement."
        else:
            suggestion = "Excellent work! Keep it up."

        # Save result
        result = Result.objects.create(
            candidate_id=candidate_id,
            total_marks=total_marks,
            percentage=percentage,
            suggestions=suggestion,
        )
        return redirect('dashboard')

    return render(request, 'quiz/quiz.html', {'questions': questions})

# Dashboard Page

def dashboard(request):
    candidate_id = request.session.get('candidate_id')
    if not candidate_id:
        return redirect('base')
    candidate = Candidate.objects.get(id=candidate_id)
    result = Result.objects.filter(candidate_id=candidate_id).first()
    
    # Pass candidate name and profession to the template
    return render(request, 'quiz/dashboard.html', {
        'candidate': candidate, 
        'result': result,
        'name': candidate.name,
        'profession': candidate.profession,  # Ensure 'profession' is a valid field in the Candidate model
    })



def report(request, report_id):
    candidate_id = request.session.get('candidate_id')
    if not candidate_id:
        return redirect('base')

    report = Report.objects.get(id=report_id)
    candidate = report.candidate
    result = report.result

    if request.method == 'POST' and not report.saved:
        report.saved = True
        report.save()
        messages.success(request, 'Your report has been saved!')
        return redirect('report', report_id=report.id)

    return render(request, 'quiz/report.html', {
        'candidate': candidate,
        'result': result,
        'report': report,
    })



def saved_reports(request):
    candidate_id = request.session.get('candidate_id')
    if not candidate_id:
        return redirect('base')
    
    # Fetch all the results (reports) for the candidate
    results = Result.objects.filter(candidate_id=candidate_id)
    
    return render(request, 'quiz/saved_reports.html', {'results': results})