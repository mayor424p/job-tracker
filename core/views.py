from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.db.models import Count, Q 
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, JobApplicationForm, InterviewForm, CustomLoginForm
from .models import jobApplication, StatusHistory, interviewLog
from django.contrib.auth.views import LoginView, LogoutView
import re
from docx import Document
import PyPDF2


def home(request):
    return render(request, "core/landing.html")


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    
    else:
        form = SignUpForm()
    return render (request, 'core/signup.html', {'form':form})



def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')

    
def dashboard_view(request):
    return render(request, 'core/dashboard.html')

@login_required
def job_list(request):
    query = request.GET.get('q', '')
    jobs = jobApplication.objects.filter(user=request.user)

    if query:
        jobs = jobs.filter(
            Q(role__icontains=query) |
            Q(company__icontains=query) |
            Q(status__icontains=query) |
            Q(date_applied__icontains=query)
        )
    return render(request, 'core/job_list.html', {'jobs': jobs, 'query': query})


@login_required
def job_detail(request, pk):
    job = get_object_or_404(jobApplication, pk=pk, user=request.user)
    return render(request, 'core/job_detail.html', {'job': job})

@login_required
def add_job(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            return redirect('job_list')
    else:
        form = JobApplicationForm()
    return render(request, 'core/add_job.html', {'form': form})

@login_required
def edit_job(request, pk):
    job = get_object_or_404(jobApplication, pk=pk, user=request.user)
    old_status = job.status

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, instance=job)
        if form.is_valid():
            updated_job = form.save(commit=False)
            new_status = updated_job.status

            if old_status != new_status:
                StatusHistory.objects.create(
                    job=job,
                    old_status=old_status,
                    new_status=new_status,
                    note=f'Status updated by {request.user.username}'           
                    )
            updated_job.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobApplicationForm(instance=job)
    return render(request, 'core/edit_job.html', {'form': form})

@login_required
def delete_job(request, pk):
    job = get_object_or_404(jobApplication, pk=pk, user=request.user)
    if request.method == 'POST':
        job.delete()
        return redirect('job_list')
    return render(request, 'core/delete_job.html', {'job': job})


@login_required
def add_interview(request, pk):
    job = get_object_or_404(jobApplication, pk=pk, user=request.user)
    if request.method == "POST":
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.job = job
            interview.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = InterviewForm()
    return render(request, 'core/interview_form.html', {'form': form, 'job': job})



@login_required
def dashboard_view(request):
    jobs = jobApplication.objects.filter(user=request.user)

    #summary counts
    total = jobs.count()
    applied = jobs.filter(status='applied').count()
    interview = jobs.filter(status='interview').count()
    offered = jobs.filter(status='offered').count()
    rejected = jobs.filter(status='rejected').count()

    #pie chart data for job status
    status_counts = (
        jobs.values('status')
        .annotate(count=Count('status'))
    )
    statuses = [s['status'] for s in status_counts]
    counts = [s['count'] for s in status_counts]

    #Monthly applications for bar chart
    monthly_apps = (
        jobs.extra(select = {'month': "strftime('%%Y - %%m', date_applied)"})
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    months = [m['month'] for m in monthly_apps]
    month_counts = [m['count'] for m in monthly_apps]

    interview_counts = (
        interviewLog.objects.filter(job__user=request.user)
        .extra(select={'month': "strftime('%%Y - %%m', interview_date)"})
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    interview_months = [i['month'] for i in interview_counts]
    interview_data = [i['count'] for i in interview_counts]

    recent_jobs = jobs.order_by('-created_at')[:5]



    return render(request, 'core/dashboard.html', {
        'total': total,
        'applied': applied,
        'interview': interview,
        'offered': offered,
        'rejected': rejected,
        'jobs': jobs,

        #charts
        'statuses': statuses,
        'counts': counts,
        'months': months,
        'month_counts': month_counts,
        'interview_months': interview_months,
        'interview_data': interview_data,
        'recent_jobs': recent_jobs,
    })

def extract_text_from_resume(file):
    #extract text from pdf or docx resume
    if file.name.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif file.name.endswith('.docx'):
        doc = Document(file)
        return "".join([para.text for para in doc.paragraphs]) 
    return ""

def analyze_resume(resume_text, job_desc):
    resume_words = set(re.findall(r'\w+', resume_text.lower()))
    job_words = set(re.findall(r'\w+', job_desc.lower()))

    common_words = resume_words & job_words
    missing_keywords = list(job_words - resume_words)

    score = round(len(common_words) / len(job_words) * 100, 2) if job_words else 0

    suggestions = "try to include more of the missing keywords in your resume." if missing_keywords else "Your resume matches well with the job description."

    return {
        "score": score,
        "missing_keywords": missing_keywords[:10],
        "suggestions": suggestions
    }


def resume_analysis(request):
    analysis = None
    if request.method == 'POST':
        resume_file = request.FILES.get('resume')
        job_desc = request.POST.get('job_desc', '')

        if resume_file and job_desc:
            resume_text = extract_text_from_resume(resume_file)
            analysis = analyze_resume(resume_text, job_desc)

    return render(request, 'core/resume_analysis.html', {'analysis': analysis})


class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    authentication_form = CustomLoginForm
# Create your views here.
from django.http import JsonResponse
from .models import jobApplication

