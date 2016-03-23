from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from ultimatereview.forms import UserForm, UserProfileForm, UpdateProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from models import Review, Researcher, Query, Paper
from django.template.defaultfilters import slugify
import search
import datetime
import json

def index(request):
    return render(request, 'ultimatereview/index.html',{})

def about(request):
    return render(request, 'ultimatereview/about.html',{})

@login_required
def myprofile(request):
    user = request.user
    form = UserForm(initial={'username':user.username, 'email':user.email, 'password':user.password})
    if request.method == 'POST':

            user.username = request.POST['username']
            user.email = request.POST['email']
            if request.POST['password'] != "":
                user.set_password(request.POST['password'])
            user.save()
    form = UserForm(initial={'username':user.username, 'email':user.email, 'password':user.password})
    context = {
        "form": form
    }
    return render(request, 'ultimatereview/myprofile.html', context)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
            'ultimatereview/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/ultimatereview/')
            else:
                return HttpResponse("Your Ultimate Review account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'ultimatereview/login.html', {})

@login_required
def myreviews(request):
	reviews = Review.objects.filter(user=request.user).order_by('-date_started')
	context = {'reviews':reviews, 'alert_message':None}
	if request.method == "POST":
		if not request.POST.get('review', "")=="":
			if not any(c in '!@#$%^&*\"\'' for c in request.POST.get('review', "")):
				if not reviews.filter(slug=slugify(request.POST.get('review', ""))).exists():
					review = Review.objects.create(user=request.user, title=request.POST.get('review', ""), date_started=datetime.datetime.now())
					review.save()
					reviews = Review.objects.filter(user=request.user).order_by('-date_started')
					context['reviews']=reviews
				else:
					context['alert_message']="A review with this name already exists."
			else:
				context['alert_message']="Title cannot contain !@#$%^&*\"\'"
		elif request.POST.get('delete_review', "")!="":
			review_to_delete=Review.objects.get(slug=request.POST.get('delete_review'))
			if review_to_delete!=None:
				review_to_delete.delete()
				context['alert_message'] = "Review deleted: "+review_to_delete.title
		else:
			context['alert_message'] = "You must give your new review a title."
	return render(request, 'ultimatereview/myreviews.html', context)

@login_required
def edit_review(request, review_name_slug):
	review=Review.objects.get(slug=review_name_slug)
	context={'title':review.title, 'slug':review.slug, 'alert_message':None}
	if request.method == 'POST':
		if review!=None:
			if not any(c in '!@#$%^&*\"\'' for c in request.POST.get('review', "")):
				if not Review.objects.filter(slug=slugify(request.POST.get('review', ""))).exists():
					review.title = request.POST.get('review', "")
					review.save()
					reviews = Review.objects.filter(user=request.user).order_by('-date_started')
					context = {'reviews':reviews, 'alert_message':"Review successfully renamed"}
					return render(request, 'ultimatereview/myreviews.html', context)
				else:
					context['alert_message']="A review with this name already exists."
			else:
				context['alert_message']="Title cannot contain !@#$%^&*\"\'"
		else:
			context['alert_message'] = "You must give your review a title."
	return render(request, 'ultimatereview/editreview.html', context)

@login_required
def single_review(request, review_name_slug):
    context = {}
    try:
        review = Review.objects.get(slug=review_name_slug)
        context['review_title'] = review.title
        queries = Query.objects.filter(review=review)
        context['queries'] = queries
        context['review'] = review
        if request.method == "POST":
            if request.POST.get('delete_query', "") != "":
                query_to_delete = Query.objects.get(name=request.POST.get('delete_query'))
                if query_to_delete != None:
                    query_to_delete.delete()
                    context['alert_message'] = "Query deleted: " + query_to_delete.name
            elif not queries.filter(name = request.POST.get('queryField')).exists():
                query = Query.objects.create(review=review, name=request.POST.get('queryField'))
                query.save()
                review = Review.objects.get(slug=review_name_slug)
                queries = Query.objects.filter(review=review)
                context['queries'] = queries
                context['review'] = review
                context['alert_message'] = "Query saved: " + request.POST.get('queryField')
    except Review.DoesNotExist:
        pass
    return render(request, 'ultimatereview/querybuilder.html', context)

@login_required
def AbstractPool(request, review_name_slug):
      papers = Paper.objects.filter().all()
      review = Review.objects.get(slug=review_name_slug)
      if request.method == "POST":
        q = request.POST.get('queryField')
        abstractList = search.main(q,"relevance", "10")
        relevance = request.POST.get("Relevancy")
        if relevance != None:
            for s in abstractList:
                if s.get('abstract') == relevance:
                    currentDoc = s
                    paper = Paper(review=review, title = currentDoc["Title"], url = currentDoc["url"], abstract = currentDoc["abstract"], author = currentDoc["Author"], abstract_relevance = "Yes" )
                    paper.save()
        return render(request, 'ultimatereview/AbstractPool.html', {"Abstracts": abstractList, 'query': q})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/ultimatereview/')

def indexQueried(request):
    if request.method == "POST":
        query = request.POST["queryField"]
        abstractList = search.main(query,"relevance","5")
        output = ""
        for i in abstractList:
            output += "Title: " + str(i['title'])
            output += "\n"
            output += "Author: " + str(i['author'])
            output += "\n"
            output += "URL: " + str(i['url'])
            output += "\n"
            output += str(['abstract'])
            output += "\n\n"
        return HttpResponse(output)
