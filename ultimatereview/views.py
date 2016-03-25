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
					review = Review(user=request.user, title=new_title, date_started=datetime.datetime.now(), pool=0)
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

def query_results(request):
	review_slug=request.POST.get('review_slug', default=None)
	if request.method == "POST" and review_slug != None:
		q = request.POST.get('queryField')
		s = request.POST.get('sortType')
		n = request.POST.get('noResults')
		abstractList = search.main(q,s, n)
	review=Review.objects.get(user=request.user, slug=review_slug)
	return render(request, 'ultimatereview/query_results.html', {'Abstracts':abstractList, 'query':q, 'review':review, 's':s, 'n':n})
	
@login_required
def AbstractPool(request, review_name_slug):
	current_review = Review.objects.get(user=request.user, slug=review_name_slug)
	if request.method == "POST":
		#the code below was moved to query results but I cannot tell what the else clause is for
        #if request.POST.get('results') == None:
        #    q = request.POST.get('queryField')
        #    s = request.POST.get('sortType')
        #    n = request.POST.get('noResults')
        #    abstractList = search.main(q,s, n)
        #else:
        #    abstractList = eval(request.POST.get('results'))
        #    q = request.POST.get('queryField')
		
		#the if below checks if the 'query' field has been sent
		#if it has, then this is a request from query_results to save all
		#however passing the abstracts from the template was problematic, because
		#the entire dictionary was turned into unicode
		#so I pass the search parameters, search again and save the results
		query=request.POST.get('query', default="")
		if query!="":
			q = request.POST.get('query')
			s = request.POST.get('s')
			n = request.POST.get('n')
			abstractList = search.main(q, s, n)
			for abstract in abstractList:
				#this turns the list of authors into a single string, separated by;
				authors_list=""
				for author in abstract.get('author'):
					authors_list=authors_list+author+";"
				paper=Paper(review=current_review, title=abstract.get("title"), paper_url=abstract.get("url"), full_text=abstract.get('fullText'), abstract=abstract.get("abstract"), authors=authors_list)
				paper.save()
			#updating the review as well
			current_review.query_string=query
			current_review.pool=1
			current_review.save()
		#else check if this is a request from the abstract pool for an abstract having been rated
		elif request.POST.get("relevanceField") == "relevant":
			#relevant abstracts have their abstract_relevance set to "True" (string)
			current_paper=Paper.objects.get(id=request.POST.get("hiddenCompareCount"))
			current_paper.abstract_relevance="True"
			current_paper.save()
			#updating the number of abstracts judged
			current_review.abstracts_judged=current_review.abstracts_judged+1
			current_review.save()
		elif request.POST.get("relevanceField") == "irrelevant":
			#id is unique among all Paper objects in the database (the database taked care of this) so it is a fast and proper identifier
			Paper.objects.get(id=request.POST.get("hiddenCompareCount")).delete()#irrelevant abstracts are deleted from the database
			current_review.abstracts_judged=current_review.abstracts_judged+1
			current_review.save()
	abstractList=Paper.objects.filter(review=current_review, abstract_relevance="False")
	if abstractList.count()==0:
		#if the abstract pool is empty, then the user must move on to the document pool
		current_review.pool=2
		current_review.save()
		documents = Paper.objects.filter(review=current_review, document_relevance="False")
		context={'documents':documents, 'review_slug':review_name_slug}
		return render(request, 'ultimatereview/document_pool.html', context)
	submitList=[]
	for abstract in abstractList:
		submitList.append({'paper':abstract, 'authors':abstract.authors.split(';')})
	return render(request, 'ultimatereview/AbstractPool.html', {"Abstracts": submitList})

@login_required
def document_pool(request, review_name_slug):
	current_review = Review.objects.get(user=request.user, slug=review_name_slug)
	context={'alert_message':None}
	if request.method == 'POST':
		if request.POST.get('relevant', "") != "":
			paper=Paper.objects.filter(paper_url=request.POST.get('relevant')).first()
			if paper!=None:
				paper.document_relevance="True"
				paper.save()
				#updating the number of documents judged
				current_review.documents_judged=current_review.documents_judged+1
				current_review.save()
				context['alert_message']="Paper "+paper.title+" was marked as relevant."
		elif request.POST.get('not_relevant', default="")!="":
			paper=Paper.objects.filter(paper_url=request.POST.get('not_relevant', "")).first()
			if paper!=None:
				paper.delete()
				current_review.documents_judged=current_review.documents_judged+1
				current_review.save()
				context['alert_message']="Paper "+paper.title+" was marked as not relevant."
	documents = Paper.objects.filter(review=current_review, document_relevance="False")
	if documents.count()==0:
	#if there are no more unrated papers, then the user moves on to the final pool
		current_review.pool=3
		current_review.save()
		documents = Paper.objects.filter(review=current_review)
		context={'documents':documents}
		return render(request, 'ultimatereview/final_pool.html', context)
	context={'documents':documents, 'review_slug':review_name_slug}
	return render(request, 'ultimatereview/document_pool.html', context)

@login_required
def final_pool(request, review_name_slug):
#displays the final pool
	current_review = Review.objects.get(user=request.user, slug=review_name_slug)
	documents = Paper.objects.filter(review=current_review)
	context={'documents':documents}
	return render(request, 'ultimatereview/final_pool.html', context)
	
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/ultimatereview/')

def indexQueried(request):
    if request.method == "POST":
        query = request.POST["queryField"]
        abstractList = search.main(query,"relevance","5")
        return render(request, 'ultimatereview/quickquery.html', {"abstracts": abstractList})
