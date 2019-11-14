from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Course
from django.db.models import Q
from itertools import chain
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

# will need to check if logged-in
def index(request):
    #return HttpResponse('Hello');
    courses = Course.objects.all()
    prefixes = courses.distinct('course_prefix')
    subjects = courses.distinct('subject')
    teachers = courses.distinct('teacher')

    context = {
        "test": 'Test Context',
        "courses": courses,
        "prefixes": prefixes,
        "subjects": subjects,
        "teachers": teachers
    }
    return render(request, "courses/index.html", context)

# name needs to be changed because it is same as django auth function
def login_view(request):
    # may want to handle both GET and POST for this later
    if request.method == 'GET':
        return render(request, 'courses/login.html')
    #return render(request, "courses/login.html")
    # for now will hanlde a POST for redirect from profile
    username = request.POST['username']
    # add try except maybe
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('profile'))
    else:
        return render(request, 'courses/login.html', {"message":'Invalid credentials'})

# allows user to sign up so they can enroll in courses
def register(request):
    if request.method == 'GET':
        return render(request, 'courses/register.html')
    else:
        #self.cleaned_data['password'], will want to clean data from all form submissions
        # handle form submission
        if request.POST['username']:
            username = request.POST['username']
        else:
            message = 'No username provided'
            return render(request, 'courses/register.html', {"message": message})
       
        if request.POST['email']:
            email = request.POST['email']
        else:
            message = 'No email provided'
            return render(request, 'courses/register.html', {"message": message})
        # add try except maybe
        if request.POST['password']:
            password = request.POST['password']
        else:
            message = 'No password provided'
            return render(request, 'courses/register.html', {"message": message})
        if request.POST['password_confirm']:
            password_confirm = request.POST['password_confirm']
        else:
            message = 'Please confirm you password'
            return render(request, 'courses/register.html', {"message": message})
        if password != password_confirm:
            message = 'Your passwords do not match'
            return render(request, 'courses/register.html', {"message": message})
        
        #new_user_password = make_password(password)
        new_user = User.objects.create_user(username, email, password)
        new_user.save()
        
        context = {
            "new": new_user.username
        }

        
            #"form": [username, password, password_confirm],
           
        return render(request, 'courses/register.html', context)




def logout_view(request):
    logout(request)
    return render(request, 'courses/login.html', {"message":'Logged Out'})

# takes search post and show results of courses, if any
def course_results(request):
    courses = Course.objects.all()
    results_list = []
    if request.GET['keyword']:
        q = request.GET['keyword']
        keyword_search = courses.filter(Q(course_name__icontains=q) | Q(subject__icontains=q) | Q(description__icontains=q))
        results_list.append(keyword_search)
    if 'prefix' in request.GET:
        prefix_search = courses.filter(course_prefix=request.GET['prefix'])
        results_list.append(prefix_search)
    if 'subject' in request.GET:
        subject_search = courses.filter(subject=request.GET['subject'])
        results_list.append(subject_search)
    if 'teacher' in request.GET:
        teacher_search = courses.filter(teacher=request.GET['teacher'])
        results_list.append(teacher_search)
    if request.GET['available'] != 'both':
        available_search = courses.exclude(course_open=request.GET['available'])
        # you may not need to append 
        results_list.append(available_search)
    # you may want to try this later to filter the results into one list
    final_results_list = list(chain(*results_list))
    final_results_list = set(final_results_list)
    #list(set().union(results_list))#list(chain(results_list))
    
    #student = request.user
    print(f'Final results: {final_results_list}')
    context = {
        "courses":courses,
        "results": final_results_list,
        #"testing": values_test

        
    }
    return render(request, "courses/course_results.html", context)
    

# gets course details, when clicked from courses results, and has register button
# add view details option from profile page
def course(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        raise Http404('Course not found.')
    context = {
        "course": course,
    }
    return render(request, 'courses/course.html', context)

def enroll(request, course_id):
    # check if user is logged in, may want to add decorator to these type of routes
    if not request.user.is_authenticated:
        return render(request, "courses/login.html", {"message":"You must be logged in to enroll in a course."})

    # gets current course, and student/all of currently enrolled courses
    course = Course.objects.get(pk=course_id)
    student = request.user
    courses = student.student.all()

    # check if student is already enrolled, if not, add course
    if course not in courses:
        student.student.add(course)
        #return HttpResponseRedirect(reverse('profile'))
        context = {
            "course": course,
            "message": "You have successfully enrolled in this course.",
            "success": True
        }
        return render(request, 'courses/confirmation.html', context)
    else:
        #return render(request, "courses/login.html", {"message":"You are already enrolled in this course."})
        context = {
            "course": course,
            "message": "You are already enrolled in this course.",
            "success": False
        }
        return render(request, 'courses/confirmation.html', context)


# allows student to unenroll if registered
# maybe add this option to profile page
@login_required
def unenroll(request, course_id):
    # check if user is logged in, may want to add decorator to these type of routes
    if not request.user.is_authenticated:
        return render(request, "courses/login.html", {"message":"You must be logged in to unenroll from a course."})

    # gets current course, and student/all of currently enrolled courses
    course = Course.objects.get(pk=course_id)
    student = request.user
    try:
        unenroll_course = student.student.get(id=course_id)
        #unenroll_course = course.objects.filter
        print(f"\nStudent is: {student}\n")
        print(f'The course is {unenroll_course} and the course is {course}')
        #print(f"student.student.course is: {student.student.all()}")

        # check if student is already enrolled, if not, add course
        if unenroll_course:
            # delete record if in studetns enrolled courses
            #unenroll_course.delete()
            student.student.remove(unenroll_course)
            #return HttpResponseRedirect(reverse('profile'))
            context = {
                "course": course,
                "message": "You have successfully unenrolled from this course.",
                "success": True
            }
            return render(request, 'courses/confirmation.html', context)
    except:
        #return render(request, "courses/login.html", {"message":"You are not enrolled in this course."})
        context = {
            "course": course,
            "message": "You are not enrolled in this course.",
            "success": False
        }
        return render(request, 'courses/confirmation.html', context)

# shows student profile with list of courses enrolled in, if any
# if not authenticated, will render login form
# for now, use profile as login test, but should be handled by login view later
# which will render the form if GET, and process from if POST and logic should
# be in login view
def profile(request):
    if not request.user.is_authenticated:
        return render(request, "courses/login.html", {"message":"Please log in to view profile."})
    student = request.user
    courses = student.student.all()
    context = {
        "student": student,
        "courses": courses,
    }

    return render(request, 'courses/profile.html', context)
