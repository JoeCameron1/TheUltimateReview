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
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print user_form.errors
    else:
        user_form = UserForm()
    return render(request,
            'ultimatereview/register.html',
            {'user_form': user_form, 'registered': registered} )

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
                return render(request, 'ultimatereview/login.html',{'alert_message':"Your Ultimate Review account is disabled."})
        else:
            return render(request, 'ultimatereview/login.html', {'alert_message':"Invalid login details."})
    else:
        return render(request, 'ultimatereview/login.html', {})

@login_required
def myreviews(request):
	reviews = Review.objects.filter(user=request.user).order_by('-date_started')
	context = {'reviews':reviews, 'alert_message':None}
	if request.method == "POST":
		new_title=request.POST.get('review', "")
		new_title = new_title.strip()
		if new_title!="":
			if not any(c in '!@#$%^&*\"\'' for c in new_title):
				if not reviews.filter(slug=slugify(new_title)).exists():
					review = Review(user=request.user, title=new_title, date_started=datetime.datetime.now())
					review.save()
					reviews = Review.objects.filter(user=request.user).order_by('-date_started')
					context['reviews']=reviews
					context['alert_message']="A review was created with name: "+new_title
				else:
					context['alert_message']="A review with this name already exists."
			else:
				context['alert_message']="Title cannot contain !@#$%^&*\"\'"
		elif request.POST.get('delete_review', "")!="":
			review_to_delete=reviews.get(slug=request.POST.get('delete_review'))
			if review_to_delete!=None:
				review_to_delete.delete()
				context['alert_message'] = "Review deleted: "+review_to_delete.title
		else:
			context['alert_message'] = "You must give your new review a title."
	return render(request, 'ultimatereview/myreviews.html', context)

@login_required
def edit_review(request, review_name_slug):
	review=Review.objects.get(user=request.user, slug=review_name_slug)
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
        review = Review.objects.get(user=request.user, slug=review_name_slug)
        context['review_title'] = review.title
        queries = Query.objects.filter(review=review)
        paper = Paper.objects.filter(review=review)
        context['queries'] = queries
        context['review'] = review
        context['paper'] = paper
        if request.method == "POST":
            if request.POST.get('abstractReturn', "") != "":
                context['abstracts'] = request.POST.get('abstractReturn')
            if request.POST.get('delete_query', "") != "":
                query_to_delete = Query.objects.get(name=request.POST.get('delete_query'))
                if query_to_delete != None:
                    query_to_delete.delete()
                    context['alert_message'] = "Query deleted: " + query_to_delete.name
            elif not queries.filter(name = request.POST.get('queryField')).exists():
                query = Query.objects.create(review=review, name=request.POST.get('queryField'))
                if query != None:
                    query.save()
                review = Review.objects.get(user=request.user, slug=review_name_slug)
                queries = Query.objects.filter(review=review)
                context['queries'] = queries
                context['review'] = review
                context['alert_message'] = "Query saved: " + request.POST.get('queryField')
    except Review.DoesNotExist:

        pass
    return render(request, 'ultimatereview/querybuilder.html', context)

@login_required
def relevant_doc(request):
    docID = None
    if request.method == "GET":
        docID = request.GET['test']
    return(HttpResponse)

@login_required
def AbstractPool(request, review_name_slug):
    review = Review.objects.get(user=request.user, slug=review_name_slug)
    if request.method == "POST":
        if request.POST.get('results') == None:
            q = request.POST.get('queryField')
            s = request.POST.get('sortType')
            n = request.POST.get('noResults')
            abstractList = search.main(q,s, n)
            for document in abstractList:
                documentURL = document.get("url")
                if Paper.objects.filter(paper_url= documentURL, review= review).exists():
                    abstractList.remove(document)
        else:
            abstractList = eval(request.POST.get('results'))
            q = request.POST.get('queryField')
        relevant="Unchecked"
        if request.POST.get("relevanceField") == "relevant":
            relevant="Relevant"
        else:
            if request.POST.get("relevanceField") == "irrelevant":
                relevant="Not Relevant"
        if relevant!="Unchecked":
            print "traceA"
            compareCount_value = int(request.POST.get("hiddenCompareCount"))
            for s in abstractList:
                if s.get('compareCount') == compareCount_value:
                        currentDoc = s
                        paper = Paper(review=review, title=currentDoc["title"], paper_url=currentDoc["url"], full_text=currentDoc['fullText'], abstract=currentDoc["abstract"], authors=currentDoc["author"], abstract_relevance=relevant)
                        paper.save()
            if len(abstractList)>1:
                for abstract in abstractList:
                    if int(abstract.get('compareCount')) > compareCount_value-1:
                        abstract['compareCount'] -= 1
                del abstractList[compareCount_value-1]
            else:
                abstractList = []
                #for abstract in abstractList:
                     #if int(abstract.get('compareCount')) > compareCount_value:
                            #abstract['compareCount'] -= 1
                #del abstractList[compareCount_value]
        return render(request, 'ultimatereview/AbstractPool.html', {"Abstracts": abstractList, 'query': q, 'review':review.title})

@login_required
def document_pool(request, review_name_slug):
	current_review = Review.objects.get(user=request.user, slug=review_name_slug)
	context={'alert_message':None, 'review': current_review.title}
	if request.method == 'POST':
		if request.POST.get('relevant', "") != "":
			paper=Paper.objects.filter(paper_url=request.POST.get('relevant')).first()
			if paper!=None:
				paper.document_relevance="True"
				paper.save()
				context['alert_message']="Paper "+paper.title+" was marked as relevant."
		elif request.POST.get('not_relevant', default="")!="":
			paper=Paper.objects.filter(paper_url=request.POST.get('not_relevant', "")).first()
			if paper!=None:
				paper.delete()
				context['alert_message']="Paper "+paper.title+" was marked as not relevant."
	documents = Paper.objects.filter(review=current_review, document_relevance="False")
	context={'documents':documents, 'review_slug':review_name_slug}
	return render(request, 'ultimatereview/document_pool.html', context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/ultimatereview/')

def indexQueried(request):
    if request.method == "POST":
        query = request.POST["queryField"]
        abstractList = search.main(query,"relevance","5")
        return render(request, 'ultimatereview/quickquery.html', {"abstracts": abstractList})
