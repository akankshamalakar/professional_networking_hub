from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import date
import requests
from bs4 import BeautifulSoup
# Create your views here.

def index(request):
    return render(request,'index.html')

def admin_login(request):
    error = ""
    if request.method== 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    d={'error':error}
    return render(request,'admin_login.html',d)

def user_login(request):
    error=''
    if request.method == "POST":
        u = request.POST['uname'];
        p = request.POST['pwd'];
        user = authenticate(username=u,password=p)
        if user:
            try:
                user1 = StudentUser.objects.get(user=user)
                if user1.type == "student":
                    login(request,user)
                    error="no"
                else:
                    error="yes"
            except:
                error="yes"
        else:
            error="yes"
    d = {'error':error}
    return render(request,'user_login.html',d)

def recruiter_login(request):
    error = ''
    if request.method == "POST":
        u = request.POST['uname'];
        p = request.POST['pwd'];
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = Recruiter.objects.get(user=user)
                if user1.type == "recruiter" and  user1.status!="pending":
                    login(request, user)
                    error = "no"
                else:
                    error = "not"
            except:
                error = "yes"
        else:
            error = "yes"
    d = {'error': error}
    return render(request,'recruiter_login.html',d)

def recruiter_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        con = request.POST['contact']
        gen = request.POST['gender']
        company = request.POST['company']
        try:
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            Recruiter.objects.create(user=user, mobile=con, image=i, gender=gen,company=company, type="recruiter", status="pending")
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request,'recruiter_signup.html',d)

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = request.user
    student = StudentUser.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        gen = request.POST['gender']

        student.user.first_name = f
        student.user.last_name = l
        student.mobile = con
        student.gender = gen
        try:
            student.save()
            student.user.save()
            error = "no"
        except:
            error = "yes"

        try:
            i = request.FILES['image']
            student.image = i
            student.save()
            error = "no"
        except:
            pass

    d = {'student': student, 'error': error}
    return render(request,'user_home.html',d)

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    rcount = Recruiter.objects.all().count()
    scount = StudentUser.objects.all().count()
    return render(request,'admin_home.html',locals())


def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        gen = request.POST['gender']

        recruiter.user.first_name = f
        recruiter.user.last_name = l
        recruiter.mobile = con
        recruiter.gender = gen
        try:
            recruiter.save()
            recruiter.user.save()
            error = "no"
        except:
            error = "yes"

        try:
            i = request.FILES['image']
            recruiter.image = i
            recruiter.save()
            error = "no"
        except:
            pass

    d = {'recruiter': recruiter, 'error': error}
    return render(request,'recruiter_home.html',d)

def Logout(request):
    logout(request)
    return redirect('index')

def user_signup(request):
    error = ""
    if request.method=='POST':
       f = request.POST['fname']
       l = request.POST['lname']
       i = request.FILES['image']
       p = request.POST['pwd']
       e = request.POST['email']
       con = request.POST['contact']
       gen = request.POST['gender']
       try:
           user = User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
           StudentUser.objects.create(user=user,mobile=con,image=i,gender=gen,type="student")
           error="no"
       except:
           error="yes"
    d={'error':error}
    return render(request,'user_signup.html',d)

def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = StudentUser.objects.all()
    d = {'data':data}
    return render(request,'view_users.html',d)

def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student = User.objects.get(id=pid)
    student.delete()
    return redirect('view_users')


def delete_recruiter(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    recruiter = User.objects.get(id=pid)
    recruiter.delete()
    return redirect('recruiter_all')

def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='pending')
    d = {'data':data}
    return render(request,'recruiter_pending.html',d)

def change_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    recruiter = Recruiter.objects.get(id=pid)
    if request.method=="POST":
        s = request.POST['status']
        recruiter.status=s
        try:
            recruiter.save()
            error = "no"
        except:
            error="yes"
    d = {'recruiter':recruiter,'error':error}
    return render(request,'change_status.html',d)


def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']

        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'change_passwordadmin.html',d)


def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']

        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'change_passworduser.html',d)

def change_passwordrecruiter(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']

        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'change_passwordrecruiter.html',d)



def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='Accept')
    d = {'data':data}
    return render(request,'recruiter_accepted.html',d)

def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='Reject')
    d = {'data':data}
    return render(request,'recruiter_rejected.html',d)

def recruiter_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.all()
    d = {'data':data}
    return render(request,'recruiter_all.html',d)

def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    if request.method=='POST':
       jt = request.POST['jobtitle']
       sd = request.POST['startdate']
       ed = request.POST['enddate']
       sal = request.POST['salary']
       l = request.FILES['logo']
       exp = request.POST['experience']
       loc = request.POST['location']
       skills = request.POST['skills']
       des = request.POST['description']
       user = request.user
       recruiter = Recruiter.objects.get(user=user)
       try:
           Jobs.objects.create(recruiter=recruiter,start_date=sd,end_date=ed,title=jt,salary=sal,image=l,description=des,experience=exp,location=loc,skills=skills,creationdate=date.today())
           error="no"
       except:
           error="yes"
    d={'error':error}
    return render(request,'add_job.html',d)

def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    job = Jobs.objects.filter(recruiter=recruiter)
    d = {'job':job}
    return render(request,'job_list.html',d)


def edit_jobdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job = Jobs.objects.get(id=pid)
    if request.method == 'POST':
        jt = request.POST['jobtitle']
        sd = request.POST['startdate']
        ed = request.POST['enddate']
        sal = request.POST['salary']
        exp = request.POST['experience']
        loc = request.POST['location']
        skills = request.POST['skills']
        des = request.POST['description']

        job.title = jt
        job.salary = sal
        job.experience = exp
        job.location = loc
        job.skills = skills
        job.description = des
        try:
            job.save()
            error = "no"
        except:
            error = "yes"
        if sd:
            try:
                job.start_date = sd
                job.save()
            except:
                pass
        else:
            pass
        if ed:
            try:
                job.end_date = ed
                job.save()
            except:
                pass
        else:
            pass
    d = {'error': error, 'job': job}
    return render(request,'edit_jobdetail.html',d)

def change_companylogo(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""
    job = Jobs.objects.get(id=pid)
    if request.method == 'POST':
        cl = request.FILES['logo']
        job.image = cl
        try:
            job.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'job': job}
    return render(request,'change_companylogo.html',d)

def user_latestjobs(request):
    job = Jobs.objects.all().order_by('-start_date')
    user = request.user
    student = StudentUser.objects.get(user=user)
    data = Apply.objects.filter(student=student)
    li=[]
    for i in data:
        li.append(i.job.id)
    d = {'job':job,'li':li}
    return render(request,'user_latestjobs.html',d)

def job_detail(request,pid):
    job = Jobs.objects.get(id=pid)
    d = {'job':job}
    return render(request,'job_detail.html',d)

def applyforjob(request,pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    user = request.user
    student = StudentUser.objects.get(user=user)
    job = Jobs.objects.get(id=pid)
    date1 = date.today()
    if job.end_date < date1:
        error = "close"
    elif job.start_date > date1:
        error="notopen"
    else:
        if request.method == 'POST':
            r = request.FILES['resume']
            Apply.objects.create(job=job, student=student,resume=r,applydate=date.today())
            error="done"

    d = {'error': error}
    return render(request,'applyforjob.html',d)

def applied_candidatelist(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    data = Apply.objects.all()

    d = {'data': data}
    return render(request,'applied_candidatelist.html',d)

def latest_jobs(request):
    url = 'https://internshala.com/jobs/'
    headers = {'User-Agent': 'Mozilla/5.0'}  # Identify the user-agent to avoid blocks
    jobs = []  # List to hold all job data

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')

        for job_div in soup.find_all('div', class_='individual_internship'):
            job_data = {}

            title_div = job_div.find('div', class_='company')
            if title_div:
                title_link = title_div.find('a', class_='view_detail_button')
                if title_link:
                    job_data['title'] = title_link.get_text(strip=True)
                    job_data['url'] = title_link['href']  # Extract the URL
                else:
                    job_data['title'] = 'N/A'
                    job_data['url'] = '#'
            else:
                job_data['title'] = 'N/A'
                job_data['url'] = '#'

            job_data['company'] = title_div.find('a', class_='link_display_like_text').get_text(
                strip=True) if title_div else 'N/A'
            job_data['location'] = job_div.find('a', class_='location_link').get_text(strip=True) if job_div.find('a',
                                                                                                                  class_='location_link') else 'N/A'

            start_date = ctc = experience = 'N/A'  # initialize the variables

            for detail_item in job_div.find_all('div', class_='other_detail_item'):
                item_heading = detail_item.find('div', class_='item_heading')
                item_body = detail_item.find('div', class_='item_body')
                if item_heading and item_body:
                    heading = item_heading.get_text(strip=True)
                    body = item_body.get_text(strip=True)
                    if 'Start' in heading:
                        job_data['start_date'] = body
                    elif 'CTC' in heading:
                        job_data['ctc'] = body
                    elif 'Experience' in heading:
                        job_data['experience'] = body

            posted_date_div = job_div.find('div', class_='status-container')
            job_data['posted_date'] = posted_date_div.get_text(strip=True) if posted_date_div else 'N/A'

            jobs.append(job_data)  # Add the job data to the list

    except requests.RequestException as e:
        print(f"Error: Unable to fetch data from {url}. {e}")
    return render(request,'latest_jobs.html',locals())

def contact(request):
    return render(request,'contact.html')