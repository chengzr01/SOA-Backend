from typing import List, Dict, Optional
from backend.src.agent_manager import AgentManager
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
from django.db.models import Q

agent_manager = AgentManager()


@csrf_exempt
def search(user_request:Dict[str, str], username:str):
    '''
    Search for jobs based on the user's request.
    @param user_request: the user's request in a dictionary format.
    @return: the response to the user's request in a dictionary format.
    '''
    print(user_request)
    
    # only company name and job title are mandatory
    company = user_request["company name"]
    job_title = user_request["job title"]
    
    try:
        level = user_request["level"]
    except KeyError:
        level = None
    try:
        location = user_request["location"]
    except KeyError:
        location = None
    try:
        requirements = user_request["requirements"]
        try:
            requirements = json.loads(requirements)  # convert string to list
        except json.JSONDecodeError:
            requirements = None
    except KeyError:
        requirements = None
        
    response = []
    
    # TODO: update search query in backend agent
    backend_agent = agent_manager.get_backend_agent(username)
    backend_agent.update_user_profile(user_request)


    # Building the query
    query = Q()
    if company:
        query &= Q(corporate__iexact=company)
    if job_title:
        query &= Q(job_title__icontains=job_title)
    if level:
        query &= Q(level__iexact=level)
    if location:
        query &= Q(location__icontains=location)

    jobs = Job.objects.filter(query)

    # filter jobs based on requirements
    if requirements:
        def requirements_match(job_requirements: str, search_requirements: List[str]) -> bool:
            try:
                job_requirements_list = json.loads(job_requirements)
                return all(req in job_requirements_list for req in search_requirements)
            except json.JSONDecodeError:
                return False

        jobs = [job for job in jobs if requirements_match(job.requirements, requirements)]

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
# TODO! new argument: username
def get_response(
    user_input: str,
    username: str,  
) -> Dict[str, str]:
    """
    Respond to user's input.
    @return: the response to the user's input in a dictionary format.
    """
    
    agent = agent_manager.get_frontend_agent(username)
    if agent is None:
        return {"front end response": None, "back end response": None}
    
    complete = agent.check_key_info_completeness(user_input)
    if complete:
        query = agent.query_backend()
        # {"company": "Google", "job_title": "software engineering"}
        res = search(query, username)
        # [{"company": "Google", "job_title": "software engineering"}, {"company": "Facebook", "job_title": "data scientist"}]
        # one and only one of the front end response and back end response should be None
        return {"front end response": None, "back end response": res}
    else:
        response = agent.respond_frontend(user_input)
        return response


@csrf_exempt
def get_recommendation(
    username: str,
) -> Dict[str, str]:
    """
    Get a recommendation for the user.
    @return: the recommendation in a dictionary format.
    """
    agent = agent_manager.get_backend_agent(username)
    if agent is None:
        return {"front end response": None, "back end response": None}
    
    query = agent.query_backend()
    res = search(query, username)
    return {"front end response": None, "back end response": res}


@csrf_exempt
@login_required
# TODO! new argument: username
def response(request, username: str):
    """
    Respond to user's input.
    Request is a POST request with the user's input in the body.
    @return: the response to the user's input in a dictionary format.
    """
    agent = agent_manager.get_frontend_agent(username)
    if agent is None:
        return JsonResponse({"front end response": None, "back end response": None})
    
    user_input = request.POST.get("user_input")
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

@csrf_exempt
@login_required
# TODO! new argument: username
def flush(request, username: str):
    """
    Flush the chat history and key information.
    @return: a JSON response.
    """
    agent = agent_manager.get_frontend_agent(username)
    if agent is None:
        return JsonResponse({"message": "Agent not found.", "success": False})
    
    agent.flush()
    return JsonResponse({"message": "Chat history and key information regarding the user have been flushed.", "success": True})

@csrf_exempt
# TODO! new argument: username
def reset(request, username: str):
    '''
    delete every chat history and key information
    et '''
    agent = agent_manager.get_frontend_agent(username)
    if agent is None:
        return JsonResponse({"message": "Agent not found.", "success": False})
    
    agent.reset()
    return JsonResponse({"message": "All chat history and key information have been reset.", "success": True})

@csrf_exempt
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
    
    # TODO? : Really need to add frontend agent and backend agent here
    # if we have already added frontend agent and backend agent in on_user_logged_in?
    # disable for now
    
    # agent_manager.add_frontend_agent(username, agent)
    # agent_manager.add_backend_agent(username, agent)
    
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

@csrf_exempt
@receiver(user_logged_in)
# TODO! new argument: username
def on_user_logged_in(sender, request, user: User, username: str, **kwargs):
    """
    Log the user's chat history in the database when the user logs in.
    """
    # print("User logged in: ", user) #DEBUG
    agent_manager.add_frontend_agent(username, user)
    agent_manager.add_backend_agent(username, user)

