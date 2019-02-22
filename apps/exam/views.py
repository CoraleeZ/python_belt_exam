from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import bcrypt
import datetime

def index(request):
    pass
    return render(request,'exam/lr.html')

def register(request):
    if request.method=='POST':
        errors=users.objects.basic_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request,value,extra_tags='red')
            return redirect('/')
        else:
            
            request.session['fn']=request.POST['fn']
            pwhash=bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())
            a=users.objects.create(first_name=request.POST['fn'],last_name=request.POST['ln'],email=request.POST['em'],password=pwhash)
            request.session['id']=a.id
        return redirect('/dashboard')


def login(request):
    if request.method=='POST':
        if users.objects.filter(email=request.POST['em']):
            a=users.objects.get(email=request.POST['em'])
            if bcrypt.checkpw(request.POST['pw'].encode(), a.password.encode()):
                request.session['id']=a.id
                request.session['fn']=a.first_name
                messages.success(request, "Successfully registered(or log in)!" ,extra_tags='green')
                return redirect('/dashboard') 
        else:
            messages.error(request,'Not valid! Try again!',extra_tags='red')
            return redirect('/')

####################################################33
def dashboard(request):
    if 'id' in request.session and 'fn' in request.session:
        if users.objects.filter(id=request.session['id']):
            a=users.objects.get(id=request.session['id'])
            if a.first_name==request.session['fn']:
                 ####validate login###
                u=users.objects.get(id=request.session['id'])
                ut=u.mytrip.all()
                revers_mytrip=[]
                for x in ut:
                    revers_mytrip.insert(0,x)
                ###reverse my trip###

                b=u.jointrip.all()
                f=u.mytrip.all()
                
                join_trip={}
                for x in b:
                    join_trip[x.id]=1
                for x in f:
                    join_trip[x.id]=1
                #######join_trip
                other_trip=[]
                e=trips.objects.all()
                for y in e:
                    if not y.id in join_trip:
                        other_trip.append(y)
                #########other trip
                context={
                    'users':u,
                    'create_trips':revers_mytrip,
                    'join_trips':b,
                    'other_trips':other_trip
                }
                return render(request,'exam/dashboard.html',context)
                 ####validate login###
    else:
        messages.error(request,'You are not log in yet!', extra_tags='red')
        return redirect('/')
########################################################################


def logout(request):
    del request.session['fn']
    del request.session['id']
    return redirect('/')


def newtrip(request):
    if 'id' in request.session and 'fn' in request.session:
        if users.objects.filter(id=request.session['id']):
            a=users.objects.get(id=request.session['id'])
            if a.first_name==request.session['fn']:
                ####validate login###
                context={
                    'users':users.objects.get(id=request.session['id'])
                }
                return render(request,'exam/create_trip.html',context)
                ####validate login###
    else:
        messages.error(request,'You are not log in yet!', extra_tags='red')
        return redirect('/')

def trips_new_process(request):
    if 'id' in request.session and 'fn' in request.session:
        if users.objects.filter(id=request.session['id']):
            a=users.objects.get(id=request.session['id'])
            if a.first_name==request.session['fn']:
                ####validate login##
                if request.method=='POST':
                    errors=trips.objects.basic_validator(request.POST)
                    if len(errors)>0:
                        for key, value in errors.items():
                            messages.error(request,value,extra_tags='red')
                        return redirect('/trips/new')
                    else:
                        u=users.objects.get(id=request.session['id'])
                        trips.objects.create(destination=request.POST['destination'],start_date=request.POST['start'],end_date=request.POST['end'],plan=request.POST['plan'],user_create=u)
                    return redirect('/dashboard')
                  ####validate login###
    else:
        messages.error(request,'You are not log in yet!', extra_tags='red')
        return redirect('/')



def edit_trip(request,trip_edit_id):
    if 'id' in request.session and 'fn' in request.session:
        if users.objects.filter(id=request.session['id']):
            a=users.objects.get(id=request.session['id'])
            if a.first_name==request.session['fn']:
                ####validate login###
                t=trips.objects.get(id=trip_edit_id)
                context={
                    'trips':t
                }
                return render(request,'exam/edit.html',context)
                ####validate login###
    else:
        messages.error(request,'You are not log in yet!', extra_tags='red')
        return redirect('/')

def edit_process(request,edit_id):
    if 'id' in request.session and 'fn' in request.session:
        if users.objects.filter(id=request.session['id']):
            a=users.objects.get(id=request.session['id'])
            if a.first_name==request.session['fn']:
                ####validate login##
                if request.method=='POST':
                    errors=trips.objects.basic_validator(request.POST)
                    if len(errors)>0:
                        for key, value in errors.items():
                            messages.error(request,value,extra_tags='red')
                        return redirect('/trips/edit/'+str(edit_id))
                    else:
                        u=users.objects.get(id=request.session['id'])
                        t=trips.objects.get(id=edit_id)
                        t.destination=request.POST['destination']
                        t.start_date=request.POST['start']
                        t.end_date=request.POST['end']
                        t.plan=request.POST['plan']
                        t.user_create=u
                        t.save()
                    return redirect('/dashboard')
                  ####validate login###
    else:
        messages.error(request,'You are not log in yet!', extra_tags='red')
        return redirect('/')




def show_trip_info(request,trip_show_id):
    if 'id' in request.session and 'fn' in request.session:
        if users.objects.filter(id=request.session['id']):
            a=users.objects.get(id=request.session['id'])
            if a.first_name==request.session['fn']:
                ####validate login###
                t=trips.objects.get(id=trip_show_id)
                
                context={
                    'users':users.objects.get(id=request.session['id']),
                    'trips':t,
                    'join':t.user_join.all()
                }
                return render(request,'exam/show_trip.html',context)
                ####validate login###
    else:
        messages.error(request,'You are not log in yet!', extra_tags='red')
        return redirect('/')


def remove(request,removeid):
    if 'id' in request.session and 'fn' in request.session:
        if users.objects.filter(id=request.session['id']):
            a=users.objects.get(id=request.session['id'])
            if a.first_name==request.session['fn']:
                ####validate login###
                t=trips.objects.get(id=removeid)
                t.delete()
                return redirect('/dashboard')
                ####validate login###
    else:
        messages.error(request,'You are not log in yet!', extra_tags='red')
        return redirect('/')





def cancel(request,cancelid):
    if 'id' in request.session and 'fn' in request.session:
        if users.objects.filter(id=request.session['id']):
            a=users.objects.get(id=request.session['id'])
            if a.first_name==request.session['fn']:
                ####validate login###
                u=users.objects.get(id=request.session['id'])
                t=trips.objects.get(id=cancelid)
                t.user_join.remove(u)
                return redirect('/dashboard')

                ####validate login###
    else:
        messages.error(request,'You are not log in yet!', extra_tags='red')
        return redirect('/')


def join_trip(request,joinid):
    if 'id' in request.session and 'fn' in request.session:
        if users.objects.filter(id=request.session['id']):
            a=users.objects.get(id=request.session['id'])
            if a.first_name==request.session['fn']:
                ####validate login###
                u=users.objects.get(id=request.session['id'])
                t=trips.objects.get(id=joinid)
                t.user_join.add(u)
                return redirect('/dashboard')
                ####validate login###
    else:
        messages.error(request,'You are not log in yet!', extra_tags='red')
        return redirect('/')

















# Create your views here.
