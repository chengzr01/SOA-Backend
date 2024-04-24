from typing import List, Dict, Optional
from backend.src.frontend_agent import FrontendAgent
from .models import Job  
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


agent = FrontendAgent() # we only have one agent but will update chat history everytime user changes

@csrf_exempt
def search(user_request:Dict[str, str]):
    '''
    Search for jobs based on the user's request.
    @param user_request: the user's request in a dictionary format.
    @return: the response to the user's request in a dictionary format.
    '''
    print(user_request)
    company = user_request["company name"]
    job_title = user_request["job title"]
    response = []

    jobs = Job.objects.filter(corporate__iexact=company, job_title__icontains=job_title)
    
    # Iterate over the queryset and serialize the results
    for job in jobs:
        response.append({
            "location": job.location, 
            "job_title": job.job_title,
            "level": job.level,
            "corporate": job.corporate,
            "requirements": json.loads(job.requirements)
        })

    # Return the response
    return response

@csrf_exempt
def get_response(
    user_input: str, 
    agent: FrontendAgent    
) -> Dict[str, str]:
    """
    Respond to user's input.
    @return: the response to the user's input in a dictionary format.
    """
    
    complete = agent.check_key_info_completeness(user_input)
    if complete:
        query = agent.query_backend(user_input)
        # {"company": "Google", "job_title": "software engineering"}
        res = search(query)
        # [{"company": "Google", "job_title": "software engineering"}, {"company": "Facebook", "job_title": "data scientist"}]
        # one and only one of the front end response and back end response should be None
        return {"front end response": None, "back end response": res}
    else:
        response = agent.respond_frontend(user_input)
        return response

@csrf_exempt
@login_required
def response(request):
    """
    Respond to user's input.
    Request is a POST request with the user's input in the body.
    @return: the response to the user's input in a dictionary format.
    """
    # # test
    # return  JsonResponse({"test": "test"})
    user_input = request.POST.get("user_input")
    # print(user_input)
    assert user_input is not None, "user_input is None"
    response = get_response(user_input, agent)
    return JsonResponse(response)   # Return the response as a JSON object

@csrf_exempt
def index(request):
    """
    Render the index page.
    @return: the index page.
    """
    return render(request, 'index.html')  # TODO

@login_required
def flush(request):
    """
    Flush the chat history and key information.
    @return: a JSON response.
    """
    agent.flush()
    return JsonResponse({"message": "Chat history and key information have been flushed.", "success": True})


def signup(request):
    """
    Sign up a new user.
    @return: a JSON response.
    """
    username = request.POST.get("username")
    password = request.POST.get("password")
    email = request.POST.get("email")
    user = User.objects.create_user(username = username, email=email, password=password)
    user.save()
    # try sign up
    # Log in the user
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # User is logged in successfully
        return JsonResponse({"message": "Sign up successful.", "success": True})
    else:
        # Authentication failed
        return JsonResponse({"message": "Failed to log in after sign up.", "success": False})
    
@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    """
    Log the user's chat history in the database when the user logs in.
    """
    print("User logged in: ", user) #debug
    agent.switch_user(user)
    