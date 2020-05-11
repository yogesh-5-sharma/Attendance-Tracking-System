from django.shortcuts import render , reverse

from django.http import HttpResponse,HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.db import IntegrityError

from django.utils import timezone

from .models import Student

from . import forms

# Create your views here.

daysofweek=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
availableslots=['08:00 - 09:00','09:00 - 10:00','10:00 - 11:00','11:00 - 12:00','12:00 - 13:00',
                '13:00 - 14:00','14:00 - 15:00','15:00 - 16:00','16:00 - 17:00','17:00 - 18:00']

def signup(request):
    
    if request.method == 'POST':
        form=forms.SignUpForm(request.POST)
        if form.is_valid():

            user=form.save()
            newstudent=Student(student=user,student_institution=form.cleaned_data['institution'])
            newstudent.save()
            user=authenticate(username=user.username,password=form.cleaned_data['password1'])
            login(request,user)
            return HttpResponseRedirect(reverse('ATS75:home'))

    else:
        form=forms.SignUpForm()
    
    return render( request , 'ATS75/signup.html' , {'form':form} )

@login_required
def home(request):
    user=Student.objects.get(student=request.user)
    timetable=user.ttcell_set.all()
    context={'user':user , 'daysofweek':daysofweek , 'availableslots':availableslots , 'timetable':timetable}
    return render(request , 'ATS75/home.html' , context) 

@login_required
def add_schedule(request):

    user=Student.objects.get(student=request.user)
    if request.method == 'POST':
        form=forms.AddScheduleForm(request.POST)
        if form.is_valid():
            
            user.schedule_start_date=request.POST['start_date']
            user.schedule_end_date=request.POST['end_date']
            user.threshold=request.POST['percentage_criteria']
            for cell in user.arcell_set.all():
                cell.delete()
            for cell in user.ttcell_set.all():
                cell.delete()
            for days in daysofweek:
                for slots in availableslots:
                    id="subject_"+days+"_"+slots
                    timetableentry=request.POST[id]
                    if timetableentry!="":
                        subject=user.subject_set.get(pk=timetableentry)
                        user.ttcell_set.create(
                            day=days,
                            time_slot_start=slots[:5],
                            time_slot_end=slots[-5:],
                            subject=subject,
                            user_ref=user
                        )
            user.save()

            return HttpResponseRedirect(reverse('ATS75:home'))
    else:
        if user.subject_set.count()==0:
            return HttpResponseRedirect(reverse('ATS75:add_subject'))
        form=forms.AddScheduleForm()
    
    context={
        'form':form,
        'daysofweek':daysofweek,
        'availableslots':availableslots,
        'user':user
    }
    return render( request , 'ATS75/addschedule.html', context )


@login_required
def delete_schedule(request):

    user=Student.objects.get(student=request.user)
    for data in user.arcell_set.all():
        data.delete()
    for data in user.ttcell_set.all():
        data.delete()
    for data in user.subject_set.all():
        data.delete()
    user.schedule_start_date=None
    user.schedule_end_date=None
    #user.threshold=None
    user.save()

    return HttpResponseRedirect(reverse('ATS75:home'))


@login_required
def add_subject(request):

    error_message=None

    if request.method == 'POST':
        form=forms.AddSubjectForm(request.POST)
        if form.is_valid():
            user=Student.objects.get(student=request.user)
            try:
                user.subject_set.create(
                    subject_code=form.cleaned_data['subject_code'],
                    subject_name=form.cleaned_data['subject_name'],
                    teacher_name=form.cleaned_data['teacher_name'],
                    user_ref=user
                )
                user.save()
            except (IntegrityError):
                error_message="Subject Already Exist !!. Please Check the subject code and name."
            else:
                if request.POST['addanother']=="0":
                    return HttpResponseRedirect(reverse('ATS75:add_schedule'))
                else:
                    form=forms.AddSubjectForm()
    else:
        form=forms.AddSubjectForm()
    
    return render(request , 'ATS75/addsubject.html' , {'form':form , 'error_message':error_message} )



@login_required
def show_attendance_record(request):

    user=Student.objects.get(student=request.user)
    start_date=user.schedule_start_date
    end_date=user.schedule_end_date
    todays_date=timezone.now().date()

    datesrange=[]

    # for subject wise report
    subjectreport=[] # subject,total,present,percentage,absent-left
    subjectindex={}
    timetable=user.ttcell_set.all()
    att_record=user.arcell_set.all()
    threshold=user.threshold
    days_left=[]
    days_till_curr_date=[]

    for subject in user.subject_set.all():
        subjectindex[subject]=len(subjectreport)
        subjectreport.append([ subject , 0 , 0 , 0 , 0])
        days_left.append(0)
        days_till_curr_date.append(0)

    curr_date=start_date
    while curr_date<=end_date:

        curr_day=daysofweek[curr_date.weekday()]
        cells=timetable.filter(day=curr_day)
        for cell in cells:
            idx=subjectindex[cell.subject]
            
            if curr_date<=todays_date:
                data=att_record.filter(date=curr_date,time_slot_start=cell.time_slot_start)
                subjectreport[idx][1]+=1
                days_till_curr_date[idx]+=1
                if data.count()!=0:
                    if data[0].value=='1':
                        subjectreport[idx][2]+=1
                    elif data[0].value!='0':
                        subjectreport[idx][1]-=1
                        days_till_curr_date[idx]-=1
            else:
                subjectreport[idx][1]+=1
                days_left[idx]+=1

        if curr_date<=todays_date:
            datesrange.append(curr_date)
        curr_date=curr_date+timezone.timedelta(1)
    
    for i in range(len(subjectreport)):
        row=subjectreport[i]
        row[0]=row[0].subject_code+" : "+row[0].subject_name
        if days_till_curr_date[i]!=0:
            row[3]=row[2]*100/days_till_curr_date[i]
        row[4]=row[2]+days_left[i]-(threshold*row[1])/100
        subjectreport[i]=row
        if row[4]<0:
            row[4]="You can't make it now."
        else:
            row[4]=int(row[4])
    
    context={
        'user': user,
        'datesrange': datesrange,
        'daysofweek': daysofweek,
        'availableslots': availableslots,

        # for subject wise report
        'subjectreport': subjectreport
    }

    if request.method == 'POST':
        day=request.POST['day']
        date=request.POST[day+'_date']
        userardata=user.arcell_set.filter(date=date)
        for cell in userardata:
            cell.delete()
        for cell in user.ttcell_set.all():
            if cell.day == day:
                val=None
                if day+"_GH" in request.POST:
                    val="GH"
                elif day+"_"+str(cell.time_slot_start) not in request.POST:
                    val="0"
                else:
                    val=request.POST[day+"_"+str(cell.time_slot_start)]

                user.arcell_set.create(
                    date=date,
                    time_slot_start=cell.time_slot_start,
                    time_slot_end=cell.time_slot_end,
                    value=val,
                    user_ref=user
                )
        return HttpResponseRedirect(reverse('ATS75:show_attendance_record'))
        

    return render( request , 'ATS75/showattendancerecord.html' , context )


"""
subject total present percentage absents-left

"""