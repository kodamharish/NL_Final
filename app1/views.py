from email import errors
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator
from .context_processors import custom_user,custom_subuser
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
#File Handling
from django.utils.deconstruct import deconstructible
from django.core.files.storage import FileSystemStorage
import os
from django.http import JsonResponse, HttpResponseBadRequest
#Mail Configuration
from django.core.mail import send_mail
from numberleader import settings
from django.contrib.sites.shortcuts import get_current_site


from django.shortcuts import redirect, render
from django.utils.timezone import datetime, timedelta
from django.contrib import messages
from .models import CashFlow, BalanceSheet, IncomeStatement

from decimal import Decimal, InvalidOperation
from decimal import Decimal
from django.shortcuts import render
from .models import Company, IncomeStatement
from calendar import month_abbr
from datetime import date
import calendar
import json
from datetime import datetime
from .utils import generate_token

import threading

# Create your views here.
def home(request):
    return render(request,'home.html')
def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')

def contact(request):
    return render(request,'contact_us.html')




def products_page(request):
    return render(request,'products.html')



from .context_processors import getAllCompanies
from .context_processors import getAllCompanies

from django.contrib import messages
from django.shortcuts import render, redirect

def login_old(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # Get the "Remember Me" value

        # Check if the user exists in both User and Team models
        #user = User.objects.filter(email=username).first()
        user = User.objects.filter(username=username).first()
        


        team = Team.objects.filter(username=username).first()

        if user:
            print(username,password)
            print(user.password)

            # Check if the email is verified before proceeding
            if not user.email_verified:
                messages.error(request, 'Please verify your email address before logging in.')
                return render(request, 'login.html')
            
            if check_password(password, user.password):
                print("Password is correct")
                print(password)
                # print(check_password(use))
                request.session['current_user_id'] = user.user_id
                if remember_me:
                    request.session.set_expiry(86400)  # 1 day
                else:
                    request.session.set_expiry(0)  # Session ends when browser is closed

                # Get the first_company_id using getAllCompanies function
                companies_info = getAllCompanies(request)
                current_user_company_profile1 = getAllCompanies(request)

                first_company_id = companies_info.get('first_company_id')
                current_user_company_profile2 = current_user_company_profile1.get('current_user_company_profiles')

                if user.user_type == 'admin':
                    return redirect('admin_dashboard')
                elif user.user_type == 'super_admin':
                    return redirect('super_admin_dashboard')
                # Uncomment and adjust these lines if needed
                # elif user.user_type == 'editor':
                #     return redirect('editor_dashboard')
                # elif user.user_type == 'user':
                #     return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        
        elif team:
            if check_password(password, team.password):
                request.session['current_subuser_id'] = team.subuser_id
                if remember_me:
                    request.session.set_expiry(86400)  # 1 day
                else:
                    request.session.set_expiry(0)  # Session ends when browser is closed

                if team.user_type == 'admin':
                    return redirect('admin_dashboard')
                elif team.user_type == 'editor':
                    return redirect('editor_dashboard')
                elif team.user_type == 'user':
                    return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        
        else:
            messages.error(request, 'Invalid username or password')

        return render(request, 'login.html')
    else:
        return render(request, 'login.html')





from django.contrib.auth.hashers import check_password
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # Get the "Remember Me" value

        # Try to find the user by username
        user = None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        
        team = Team.objects.filter(username=username).first()

        if user:
            # Check if the email is verified before proceeding
            if not user.email_verified:
                messages.error(request, 'Please verify your email address before logging in.')
                return render(request, 'login.html')

            # Check the password
            if (password == user.password):
                request.session['current_user_id'] = user.user_id
                if remember_me:
                    request.session.set_expiry(86400)  # 1 day
                else:
                    request.session.set_expiry(0)  # Session ends when browser is closed

                # Get the first_company_id using getAllCompanies function
                companies_info = getAllCompanies(request)
                current_user_company_profile1 = getAllCompanies(request)

                first_company_id = companies_info.get('first_company_id')
                current_user_company_profile2 = current_user_company_profile1.get('current_user_company_profiles')

                if user.user_type == 'admin':
                    return redirect('admin_dashboard')
                elif user.user_type == 'super_admin':
                    return redirect('super_admin_dashboard')
                # Uncomment and adjust these lines if needed
                # elif user.user_type == 'editor':
                #     return redirect('editor_dashboard')
                # elif user.user_type == 'user':
                #     return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        
        elif team:
            if check_password(password, team.password):
                request.session['current_subuser_id'] = team.subuser_id
                if remember_me:
                    request.session.set_expiry(86400)  # 1 day
                else:
                    request.session.set_expiry(0)  # Session ends when browser is closed

                if team.user_type == 'admin':
                    return redirect('admin_dashboard')
                elif team.user_type == 'editor':
                    return redirect('editor_dashboard')
                elif team.user_type == 'user':
                    return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        
        else:
            messages.error(request, 'Invalid username or password')

        return render(request, 'login.html')
    else:
        return render(request, 'login.html')
















def logout(request):
    request.session.flush()
    return redirect('login')

class EmailThread(threading.Thread):
    def __init__(self,email):
        self.email=email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send()

from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.core.mail import EmailMessage
from django.conf import settings

def send_activation_email(user, request):
    # Generate activation link
    current_site = get_current_site(request)
    subject = 'Activate Your Account on Number Leader'
    uid = urlsafe_base64_encode(force_bytes(user.pk))  # Encode the user's primary key
    # activation_link = f'http://{current_site.domain}/activate/{uid}/{token}/'  # Construct the activation link
    email_body=render_to_string('activate.html', {
        'user':user,
        'domain':current_site,
        'uid':uid,
        'token':generate_token.make_token(user),
    })
    email=EmailMessage(subject=subject, body=email_body, from_email=settings.EMAIL_FROM_USER, to=[user.email])
    EmailThread(email).start()
    # message = f'Dear {user.firstname},\n\nYour account has been successfully created on Number Leader.\n\nPlease activate your account by clicking the link below:\n\n{activation_link}\n\nThank you for signing up!'
    # from_email = 'prasannasgkumar@gmail.com'
    # recipient_list = [user.email]

    # # Send the email
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt  
def activate_user(request, uidb64, token):
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
      
        user = User.objects.get(pk=uid)
        
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
       
        user = None

  
    if user  and generate_token.check_token(user, token):
        user.email_verified = True
        user.save()
        messages.success(request, 'Email Verification Successful. Please log in to your account.')
        return redirect('login')
    
    return render(request, 'activation-failed.html', {'user':user})









def signup(request):
    if request.method == 'POST':
        # Extract form data
        # User Details
        username = request.POST.get('username_email')
        email = request.POST.get('username_email')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name', '')  # Optional field
        password = request.POST.get('password1')
        confirm_password = request.POST.get('confirm_password')
        
        # Company Details
        company_name = request.POST.get('company_name')
        company_type= request.POST.get('company_type')

        # Validate passwords
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('login')
        
        # Check if the username or email already exists
        if User.objects.filter(username=username).exists() or Team.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('login')
        
        if User.objects.filter(email=email).exists() or Team.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('login')

        # Create and save User object
        user = User(
            username=username,
            email=email,
            firstname=firstname,
            lastname=lastname,
            password=password,  # Make sure to hash the password before saving
        )
        print(password,'from sign up')
        user.save()

        # Ensure the user was saved correctly
        if user.pk:
            # Create and save Company object
            company = Company(
                user_id=user,  # Assuming user_id is a ForeignKey field in the Company model
                name=company_name,
                company_type=company_type
            )
            company.save()

            if company.pk:
                # Call the send_activation_email function
                send_activation_email(user, request)

                messages.success(request, 'User and company created successfully. A confirmation email has been sent.')
                return redirect('login')  # Redirect to login after successful signup
            else:
                messages.error(request, 'Something went wrong. Please try again later.')
                return redirect('login')
        else:
            messages.error(request, 'Something went wrong. Please try again later.')
            return redirect('login')
    
    # If request is GET, render the signup page
    else:
        return redirect('login')






#Super Admin
def superAdminDashboard(request):
    admins_count = User.objects.count()
    editors_count = Team.objects.filter(user_type='editor').count()
    users_count = Team.objects.filter(user_type='user').count()

    startups = User.objects.filter(company_type='Startup').count()
    investors= User.objects.filter(company_type='Investor').count()
    ca_firms= User.objects.filter(company_type='CA_firm').count()
    companys = Company.objects.count()
    context = {
        'admins_count': admins_count,
        'editors_count': editors_count,
        'users_count': users_count,
        'startups':startups,
        'investors':investors,
        'ca_firms':ca_firms,
        'companys':companys
    }

    return render(request,'super_admin/dashboard.html',context)


def startups(request):
    startups = User.objects.filter(company_type='Startup').all()
    context = {'startups':startups}
    return render(request,'super_admin/startups.html',context)

def investors(request):
    investors= User.objects.filter(company_type='Investor').all()
    context = {'investors':investors}
    return render(request,'super_admin/investors.html',context)

def ca_firms(request):
    ca_firms= User.objects.filter(company_type='CA_firm').all()
    context = {'ca_firms':ca_firms}
    return render(request,'super_admin/ca_firms.html',context)

def companies(request):
    companies = Company.objects.all()
    context ={'companies':companies}
    return render(request,'super_admin/companies.html',context)

def admins(request):
    admins = User.objects.all()
    context = {'admins':admins}

    return render(request,'super_admin/admins.html',context)

def editors(request):
    editors = Team.objects.filter(user_type='editor')
    context = {'editors':editors}

    return render(request,'super_admin/editors.html',context)

def users(request):
    users = Team.objects.filter(user_type='user')
    context = {'users':users}

    return render(request,'super_admin/users.html',context)




#Admin

def myTeam(request):
    if request.method == 'POST':
        pass          
    else:
        user_context = custom_user(request)
        current_user = user_context.get('current_user')  
        subuser_context = custom_subuser(request)
        current_subuser = subuser_context.get('current_subuser') 
        if current_user:
            total_team_data = Team.objects.filter(creator_id =current_user)
        if current_subuser:
                total_team_data = Team.objects.filter(creator_id = current_subuser)

        context = {'total_team_data':total_team_data}
        return render(request, 'admin/my_team.html',context)

def addTeam(request):
    if request.method == 'POST':
        # Extract form data using request.POST.get
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        linkedin_url = request.POST.get('linkedin_url', '')  # Optional field
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname', '')  # Optional field
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_type = request.POST.get('user_type')
        companyID = request.POST.get('company')

        
        # Validate passwords
        if password != confirm_password:
            messages.error(request,'Passwords do not match')
            return redirect('add_team')
            
        # Validate if the username or email already exists
        if Team.objects.filter(username=username).exists() or User.objects.filter(username=username).exists():
            messages.error(request,'Username already exists')
            return redirect('add_team')
            
        if Team.objects.filter(email=email).exists() or User.objects.filter(email=email).exists():
            messages.error(request,'Email already exists')
            return redirect('add_team')
        user_context = custom_user(request)
        current_user = user_context.get('current_user')  
        subuser_context = custom_subuser(request)
        current_subuser = subuser_context.get('current_subuser') 
        #creator_id = current_subuser.creator_id

        if current_user:
            # Fetch the User instance for the creator_id
              #creator_user = User.objects.get(user_id=current_user.user_id)
              creator_user = current_user.user_id
        if current_subuser:
              if current_subuser.user_type == 'editor':
                  # Fetch the User instance for the creator_id
                  #creator_user = Team.objects.get(subuser_id=current_subuser.subuser_id)
                  creator_user = current_subuser.subuser_id

        # Fetch the Company instance based on company_id
        company_id = Company.objects.get(company_id=companyID)
        # Create and save User object
        team = Team(
            username=username,
            creator_id=creator_user,
            company_id = company_id,
            email=email,
            phone_number=phone_number,
            linkedin_url=linkedin_url,
            firstname=firstname,
            lastname=lastname,
            password=password,
            user_type = user_type
        )
        
        team.save()
        # Get the current site domain
        current_site = get_current_site(request)
        domain = current_site.domain

        # Construct the Login URL
        signin_url = f'http://{domain}/login'

        subject='Number Leader Registration Details'
        txt='''Welcome to  Number Leader

               Below are your Login Details :

               First Name : {}
               First Name : {}
               Email : {}
               Username : {}
               Password : {}
               Phone Number : {}
               Linkedin URL : {}
               User Type : {}
               Company : {}

               You can Login by using below this URL : {}        
                '''
        message=txt.format(firstname,lastname,email,username,password,phone_number,linkedin_url,user_type,company_id.name,signin_url)
        from_email=settings.EMAIL_HOST_USER
        to_list=[email]
        send_mail(subject, message,from_email,to_list,fail_silently=True)
        messages.error(request,'Member Created Successfully')
        return redirect('add_team')       
           
    else:
        return render(request, 'admin/add_team.html')
    

def updateTeam(request, id):
    if request.method == 'POST':
        # Fetch the existing Team instance using subuser_id
        team = get_object_or_404(Team, subuser_id=id)

        # Extract form data using request.POST.get
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        linkedin_url = request.POST.get('linkedin_url', '')  # Optional field
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname', '')  # Optional field
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        companyID = request.POST.get('company')

        

        user_context = custom_user(request)
        current_user = user_context.get('current_user')  

        # # Fetch the User instance for the creator_id
        # creator_user = User.objects.get(user_id=current_user.user_id)

        subuser_context = custom_subuser(request)
        current_subuser = subuser_context.get('current_subuser') 

        if current_user:
            # Fetch the User instance for the creator_id
              #creator_user = User.objects.get(user_id=current_user.user_id)
              creator_user = current_user.user_id
        if current_subuser:
              if current_subuser.user_type == 'editor':
                  # Fetch the User instance for the creator_id
                  #creator_user = Team.objects.get(subuser_id=current_subuser.subuser_id)
                  creator_user = current_subuser.subuser_id


        
        # Fetch the Company instance based on company_id
        company_id = Company.objects.get(company_id=companyID)

        # Update the Team instance
        team.username = username
        team.creator_id = creator_user
        team.company_id = company_id
        team.email = email
        team.phone_number = phone_number
        team.linkedin_url = linkedin_url
        team.firstname = firstname
        team.lastname = lastname
        team.password = password
        team.user_type = user_type
        
        team.save()

        # Get the current site domain
        current_site = get_current_site(request)
        domain = current_site.domain

        # Construct the Login URL
        signin_url = f'http://{domain}/login'

        subject='Number Leader - Updated Details'
        txt='''Welcome to  Number Leader

               Below are your Updated Login Details :

               First Name : {}
               First Name : {}
               Email : {}
               Username : {}
               Password : {}
               Phone Number : {}
               Linkedin URL : {}
               User Type : {}
               Company : {}

               You can Login by using below this URL : {}        
                '''
        message=txt.format(firstname,lastname,email,username,password,phone_number,linkedin_url,user_type,company_id.company_name,signin_url)
        from_email=settings.EMAIL_HOST_USER
        to_list=[email]
        send_mail(subject, message,from_email,to_list,fail_silently=True)
        messages.success(request, 'Member Updated Successfully')
        return redirect('add_team')       
    else:
        context={'team': get_object_or_404(Team, subuser_id=id)}
        return render(request, 'admin/update_team.html',context)

def deleteTeam(request,id):
    team = get_object_or_404(Team, subuser_id=id)    
    # Delete the team member
    team.delete()
    # Show a success message
    messages.success(request, 'Member Deleted Successfully')
    return redirect('my_team')
 



def adminDashboard(request):
    startup = Company.objects.filter(company_type='startup').order_by('?')[:3]
    investor = Company.objects.filter(company_type='investor').order_by('?')[:3]
    enablers = Company.objects.filter(company_type='enablers').order_by('?')[:3]
    news = Company_news.objects.all().order_by('?')[:5]

    

    context = {
        'startup':startup,
        'enablers': enablers,
        'investor':investor,
        'news':news
      
    }
    
    return render(request,'admin/dashboard.html', context) 










def companyProfileForm(request,id):
    company = Company.objects.get(company_id = id)

    if request.method == 'POST':
        # company data
        startup_name = request.POST.get('startup_name')
        date_of_incorporation = request.POST.get('date_of_incorporation')
        email = request.POST.get('email')
        linkedin_url = request.POST.get('linkedin_url')
        sector_name = request.POST.get('sector')
        type_of_business = request.POST.get('type_of_business')
        no_of_employees = request.POST.get('no_of_employees')
        website_url = request.POST.get('website_url')
        location = request.POST.get('location')
        product_or_service = request.POST.get('product_or_service')
        subscription_type = request.POST.get('subscription_type')
        #company profile
        tam = request.POST.get('tam')
        cagr = request.POST.get('cagr')
        previous_year_revenue = request.POST.get('previous_year_revenue')
        current_year_revenue = request.POST.get('current_year_revenue')
        current_monthly_burn_rate = request.POST.get('current_monthly_burn_rate')
        forecasted_revenue_for_next_year = request.POST.get('forecasted_revenue_for_next_year')
        stage_of_business = request.POST.get('stage_of_business')
        equity_funds_raised_so_far = request.POST.get('equity_funds_raised_so_far')
        funds_needed = request.POST.get('funds_needed')
       


        #business_introductory_video_file = request.FILES.get('business_introductry_video_file')
        #business_introductory_video_url = request.POST.get('business_introductry_video_url')

        # business_plan = request.FILES.get('business_plan')
        # vision = request.POST.get('vision')
        # mission = request.POST.get('mission')
        # usp = request.POST.get('usp')

        user_context = custom_user(request)
        current_user = user_context.get('current_user') 

        sector = Sector.objects.get(name=sector_name)
        type_of_business = BusinessType.objects.get(name=type_of_business)
        stage_of_business = BusinessStage.objects.get(name=stage_of_business)

        # # Create the Company instance
        company = Company(
            user_id=current_user,  # This should match the foreign key field in Company model
            company_id = company,
            name=startup_name,
            date_of_incorporation = date_of_incorporation,
            email = email,
            linkedin_url = linkedin_url,
            sector = sector,
            business_type = type_of_business,
            website_url=website_url,
            location = location,
            company_type = product_or_service,
            subscription_type = subscription_type
            
        )
        company.save()

        # Create the CompanyProfile instance
        company_profile = CompanyProfile(
            company_id=company,
            number_of_clients_users = no_of_employees, 
            tam = tam,
            cagr = cagr,
            previous_year_revenue = previous_year_revenue,
            current_year_revenue_arr = current_year_revenue,
            current_monthly_burn_rate = current_monthly_burn_rate,
            forecasted_revenue_for_next_year = forecasted_revenue_for_next_year,
            business_stage = stage_of_business,
            equity_funds_raised_so_far = equity_funds_raised_so_far,
            funds_needed = funds_needed

        )
        company_profile.save()

        # Save founders
        founder_count = int(request.POST.get('founder_count', 1))
        for i in range(1, founder_count + 1):
            founder_name = request.POST.get(f'founder_{i}_name')
            linkedin_profile = request.POST.get(f'founder_{i}_linkedin_profile')
            short_profile = request.POST.get(f'founder_{i}_short_profile')
            phone_no = request.POST.get(f'founder_{i}_phno')
            email = request.POST.get(f'founder_{i}_email')
            photo = request.FILES.get(f'founder_{i}_photo')
            if founder_name and linkedin_profile and short_profile and phone_no and email and photo:
                founder = Founder(
                    company_id=company,
                    name=founder_name,
                    linkedin_url=linkedin_profile,
                    short_profile=short_profile,
                    phone_number=phone_no,
                    email=email,
                    photo=photo
                )
                founder.save()

        # Save executive members
        executive_member_count = int(request.POST.get('executive_member_count', 1))
        for i in range(1, executive_member_count + 1):
            executive_member_name = request.POST.get(f'executive_member_{i}_name')
            executive_member_email = request.POST.get(f'executive_member_{i}_email')
            executive_member_designation = request.POST.get(f'executive_member_{i}_designation')

            if executive_member_name and executive_member_email and executive_member_designation :
                executive_member = ExecutiveMember(
                    company_id = company,
                    name = executive_member_name,
                    email = executive_member_email,
                    designation = executive_member_designation
                    
                )
                executive_member.save()

        # Save advisors
        advisor_count = int(request.POST.get('advisor_count', 1))
        for i in range(1, advisor_count + 1):
            advisor_name = request.POST.get(f'advisor_{i}_name')
            advisor_email = request.POST.get(f'advisor_{i}_email')
            advisor_phno = request.POST.get(f'advisor_{i}_phno')

            if advisor_name and advisor_email and advisor_phno :
                advisor = Advisor(
                    company_id = company,
                    name = advisor_name,
                    email = advisor_name,
                    phonenumber = advisor_phno
                    
                )
                advisor.save()

        # Save solved problems
        problem_solved_count = int(request.POST.get('problem_solved_count', 1))
        for i in range(1, problem_solved_count + 1):
            problem_solved = request.POST.get(f'problem_solved_{i}')
            

            if problem_solved :
                solved_problem = SolvedProblem(
                    company_id = company,
                    description = problem_solved
                     
                )
                solved_problem.save()
        
        # Save challenges
        challenge_count = int(request.POST.get('challenge_count', 1))
        for i in range(1, challenge_count + 1):
            challenge = request.POST.get(f'challenge_{i}')
            

            if challenge :
                challenge = Challenge(
                    company_id = company,
                    name = challenge
                     
                )
                challenge.save()

        # Save competitors
        competitor_count = int(request.POST.get('competitor_count', 1))
        for i in range(1, competitor_count + 1):
            competitor = request.POST.get(f'competitor_{i}')
            

            if competitor :
                competitor = Competitor(
                    company_id = company,
                    name = competitor
                     
                )
                competitor.save()

    

        # Save social media URLs
        url_count = int(request.POST.get('url_count', 2))
        for i in range(1, url_count + 1):
            url = request.POST.get(f'url_{i}')
            if url:
                social_media = SocialMedia(
                    company_id=company,
                    url=url
                )
                social_media.save()

        # Save clients
        client_count = int(request.POST.get('client_count', 1))
        for i in range(1, client_count + 1):
            client_name = request.POST.get(f'client_name_{i}')
            client_logo = request.FILES.get(f'client_logo_{i}')
            if client_name and client_logo:
                client = Client(
                    company_id=company,
                    name=client_name,
                    logo=client_logo
                )
                client.save()

        return redirect('add_company')  # Redirect to a success page
    else:
        sectors = Sector.objects.all()
        business_types = BusinessType.objects.all()
        business_stages = BusinessStage.objects.all()
        context = { 'sectors':sectors,'business_types':business_types,'business_stages':business_stages,'company':company}
        return render(request,'admin/company_profile_form.html',context)


def companyProfile(request, id):
    company = get_object_or_404(Company, company_id=id)
    try:
        company_profile = CompanyProfile.objects.get(company_id=id)
    except CompanyProfile.DoesNotExist:
        company_profile = None

    

    if request.method == 'POST':
            # Company profile
            excecutive_summary = request.POST.get('excecutive_summary')
            technology_profile = request.POST.get('technology_profile')
            type_of_industry = request.POST.get('type_of_industry')
            no_of_employees = request.POST.get('no_of_employees')
            ceo = request.POST.get('ceo')
            cfo = request.POST.get('cfo')
            cmo = request.POST.get('cmo')
            vp = request.POST.get('vp')
            # Create the CompanyProfile instance and associate it with the Company instance
            company_profile = CompanyProfile(
            company_id=company,  # Associate with the newly created Company instancec
            excecutive_summary=excecutive_summary,
            technology_profile=technology_profile,
            type_of_industry=type_of_industry,
            no_of_employees=no_of_employees,
            ceo=ceo,
            cfo=cfo,
            cmo=cmo,
            vp=vp
            )
            company_profile.save()

            
            messages.success(request, 'Data saved Successfully')
            return redirect('comprehensive_profile')
    else:
        context = {'company': company,'company_profile': company_profile }
        return render(request, 'investor/basic_information.html', context)




# def businessPlan(request, id):
#     company = Company.objects.get(company_id = id)
    
#     if request.method == 'POST':
#         business_plan = request.FILES.get('business_plan')
#         new_business_plan = request.FILES.get('new_business_plan')
#         company_profile.business_plan= business_plan
       
#         if new_business_plan:
#             company_profile.business_plan= new_business_plan
#             #company_profile.save()
#         company_profile.save()

#         return redirect('businessdocs',company.company_id)

#     else:
        
#         context = {
#             'company':company,
#             'company_profile': company_profile,
#         }

#         return render(request, 'admin/businessdocs.html', context)
    

from django.db.models import Max
from django.core.files.storage import default_storage
from django.core.serializers import serialize
from django.http import JsonResponse


def businessPlan(request, id):
    
    company = Company.objects.get(company_id = id)
  

    try:
        plan_files = plan_finacials.objects.filter(company_id = id)              
        last_rec = plan_files.aggregate(Max('line_no'))['line_no__max']              
    except:
        plan_files = None        
        last_rec = None        

    try:
        products = productsandservices.objects.all()
    except:
        products = None

    context = {
        'company':company,
      
        'plan_files':plan_files,        
        'last_rec':last_rec,
        'products':products       
    }

    if request.method == 'POST':
        
        b_files = request.FILES.get('b_files')
        f_files = request.FILES.get('f_files')
        line_no = request.POST.get('line_no')
        p_name = request.POST.get('p_name')
                

        try:
            ext_file =  plan_finacials.objects.get(company_id = id, line_no = line_no)     
        except:
            ext_file = None
        
        if ext_file:
            if b_files:
                if ext_file.b_plan_pdf:                    
                    if default_storage.exists(ext_file.b_plan_pdf.path):
                        default_storage.delete(ext_file.b_plan_pdf.path)                
                ext_file.b_plan_pdf = b_files
                ext_file.p_name = p_name
                ext_file.save()

            if f_files:
                if ext_file.f_plan_pdf:                    
                    if default_storage.exists(ext_file.f_plan_pdf.path):
                        default_storage.delete(ext_file.f_plan_pdf.path)                
                ext_file.f_plan_pdf = f_files
                ext_file.p_name = p_name
                ext_file.save()      
            
        else:                              
            plan_finacials_new = plan_finacials(
                company_id = company, 
                line_no = line_no,           
                b_plan_pdf = b_files,
                f_plan_pdf = f_files,
                p_name = p_name
            )
            plan_finacials_new.save()

        return JsonResponse({'message': 'Details saved successfully!'})  

    else:
        return render(request, 'admin/businessdocs.html', context)        
    

def remove_file(request):    
    line_no = request.GET.get('line_no')
    file_type = request.GET.get('type')  # 'b' for b_plan_pdf, 'f' for f_plan_pdf
    
    if line_no is None or file_type not in ['b', 'f']:
        return JsonResponse({'error': 'Invalid request parameters.'}, status=400)
    
    # Get the plan_finacials record based on the line_no
    try:
        plan_file = get_object_or_404(plan_finacials, line_no=line_no)
    except plan_finacials.DoesNotExist:
        return JsonResponse({'error': 'File not found.'}, status=404)

    # Determine the file to delete
    if file_type == 'b':
        file_path = plan_file.b_plan_pdf.path
        plan_file.b_plan_pdf.delete(save=False)
    elif file_type == 'f':
        file_path = plan_file.f_plan_pdf.path
        plan_file.f_plan_pdf.delete(save=False)

    # Delete the file from the file system
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Check if both files are now empty and delete the record if so
    if not plan_file.b_plan_pdf and not plan_file.f_plan_pdf:
        plan_file.delete()
    else:
        plan_file.save()

    return JsonResponse({'message': 'File removed successfully.'})


# def news_post(request, id):
#     company = Company.objects.get(company_id=id)
#     company_profile = CompanyProfile.objects.get(company_id=id)
#     current_date = datetime.now().date()

#     try:
#         news_data = news.objects.filter(company_id=id)
#         last_rec = news_data.aggregate(Max('line_no'))['line_no__max']
#     except:
#         news_data = None
#         last_rec = None

#     context = {
#         'company': company,
#         'company_profile': company_profile,
#         'current_date': current_date,
#         'news_data': news_data,
#         'last_rec': last_rec
#     }

#     if request.method == 'POST':
#         line_no = request.POST.get('line_no')
#         summary = request.POST.get('summary')
#         link = request.POST.get('link')

#         try:
#             old_data = news.objects.get(company_id=id, line_no = line_no)
#         except:
#             old_data = None        

        

#         if old_data:            
#             old_data.sub_date = current_date
#             old_data.summary = summary
#             old_data.link = link
#             old_data.save()             
#             return JsonResponse({'message': 'Details updated successfully!'})     
#         else:
#             news_new = news(
#                 company_id=company,
#                 sub_date = current_date,
#                 line_no=line_no,
#                 summary=summary,
#                 link=link
#             )
#             news_new.save()
#             return JsonResponse({'message': 'Details saved successfully!'})        

#     return render(request, 'admin/news_post.html', context)


    





from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def pitchAndProduct(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            company = get_object_or_404(Company, company_id=id)
            
            # Create a new product instance
            product = productsandservices.objects.create(
                company_id=company,
                name=data.get('name'),
                launch_date=data.get('launch_date'),
                description=data.get('description'),
                industry=data.get('industry'),
                type_of_business=data.get('type_of_business'),
                problem_solved=data.get('problem_solved'),
                current_year_revenue=int(data.get('current_year_revenue')),
                previous_year_revenue=int(data.get('previous_year_revenue')),
                a_year_before_revenue=int(data.get('a_year_before_revenue')),
                current_year_pl=int(data.get('current_year_pl')),
                previous_year_pl=int(data.get('previous_year_pl')),
                a_year_before_pl=int(data.get('a_year_before_pl')),
                customers=data.get('customers'),
                competitors=data.get('competitors')
            )
            
            return JsonResponse({'status': 'success', 'id': product.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            product_id = data.get('id')
            product = get_object_or_404(productsandservices, id=product_id)
            
            # Update the product instance
            product.name = data.get('name')
            product.launch_date = data.get('launch_date')
            product.description = data.get('description')
            product.industry = data.get('industry')
            product.type_of_business = data.get('type_of_business')
            product.problem_solved = data.get('problem_solved')
            product.current_year_revenue = int(data.get('current_year_revenue'))
            product.previous_year_revenue = int(data.get('previous_year_revenue'))
            product.a_year_before_revenue = int(data.get('a_year_before_revenue'))
            product.current_year_pl = int(data.get('current_year_pl'))
            product.previous_year_pl = int(data.get('previous_year_pl'))
            product.a_year_before_pl = int(data.get('a_year_before_pl'))
            product.customers = data.get('customers')
            product.competitors = data.get('competitors')
            product.save()

            return JsonResponse({'status': 'success'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        except productsandservices.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            product_id = data.get('id')
            product = get_object_or_404(productsandservices, id=product_id)
            product.delete()
            return JsonResponse({'status': 'success'})

        except productsandservices.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    elif request.method == 'GET':
        company = get_object_or_404(Company, company_id=id)
        
        products = productsandservices.objects.filter(company_id=company)

        # Check if the request expects JSON (e.g., for AJAX)
        if request.headers.get('Accept') == 'application/json' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            products_list = list(products.values())  # Convert queryset to list of dictionaries
            return JsonResponse({'products': products_list}, status=200)

        # Otherwise, render the HTML page
        context = {
            'company': company,
            
            'products': products
        }

        return render(request, 'admin/products.html', context)



from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def capTable(request, id):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)

            
            name = data.get('name')
            shareholder = data.get('shareholder')
            percentage_of_shares = data.get('equityShare')
            investedsince = data.get('investedSince')
            amount = data.get('investmentAmount')
            valuation = data.get('valuation')
            details = data.get('details')

            # Fetch the associated company object
            company = Company.objects.get(company_id=id)

            # Create a new CapTable entry
            CapTable.objects.create(
                company_id=company,
                name=name,
                shareholder=shareholder,
                percentage_of_shares=percentage_of_shares,
                investedsince=investedsince,
                amount=amount,
                valuation=valuation,
                details=details
            )

            # Return a success response
            return redirect('cap_table', id)

        except json.JSONDecodeError:
            return redirect('cap_table', id)

        except Company.DoesNotExist:
            return redirect('cap_table', id)

    elif request.method == 'GET':
        company = Company.objects.get(company_id=id)
        company_profile = CompanyProfile.objects.get(company_id=id)
        cap_table = CapTable.objects.filter(company_id=id)

        context = {
            'company': company,
            'company_profile': company_profile,
            'cap_table': cap_table
        }

        return render(request, 'admin/cap_table.html', context)

def capTableForm(request, id):
    company = Company.objects.get(company_id = id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        linkedin_url = request.POST.get('linkedin_url')
        percentage_of_shares = request.POST.get('equityShare')
        photo = request.FILES.get('photo')

        cap_table = CapTable(
            company_id = company,
            name = name,
            email = email,
            linkedin_url = linkedin_url,
            percentage_of_shares = percentage_of_shares,
            photo = photo
        )
        cap_table.save()
        messages.success(request,'Data saved successfully')
        return redirect('cap_table',company.company_id)

    else:
        company_profile = CompanyProfile.objects.get(company_id = id)
        
    
        context = {
            'company':company,
            'company_profile': company_profile,
        }

        return render(request, 'admin/cap_table_form.html', context)



def get_period_label(begin_date, end_date):
    # Define financial quarters
    quarters = {
        'Q1': (1, 3),  # January to March
        'Q2': (4, 6),  # April to June
        'Q3': (7, 9),  # July to September
        'Q4': (10, 12)  # October to December
    }

    # Check if dates span a full year
    if begin_date == begin_date.replace(month=1, day=1) and end_date == end_date.replace(month=12, day=31):
        return f'{begin_date.strftime("%b %d, %Y")} - {end_date.strftime("%b %d, %Y")}', 'Annually Data'

    # Check if dates span more than one year
    if begin_date.year != end_date.year:
        return f'{begin_date.strftime("%b %d, %Y")} - {end_date.strftime("%b %d, %Y")}', 'Irregular Data'

    # Same month case
    if begin_date.month == end_date.month:
        return month_abbr[begin_date.month], 'Monthly Data'
    
    # Quarterly cases
    for quarter, (start_month, end_month) in quarters.items():
        if begin_date.month == start_month and end_date.month == end_month:
            months = [month_abbr[m] for m in range(start_month, end_month + 1)]
            return f'{quarter} ({", ".join(months)})', 'Quarterly Data'
    
    # Custom or irregular period
    return f'{begin_date.strftime("%b %d, %Y")} - {end_date.strftime("%b %d, %Y")}', 'Irregular Data'





def get_months_quarters_years():
    # Get all month names
    months = list(calendar.month_name)[1:]  # Exclude empty string at index 0
    
    # Define quarters
    # quarters = {
    #     'Q1': months[0:3],   # January, February, March
    #     'Q2': months[3:6],   # April, May, June
    #     'Q3': months[6:9],   # July, August, September
    #     'Q4': months[9:12]   # October, November, December
    # }

    # Define quarters with month names
    quarters = [
        "Jan,Feb,Mar",
        "Apr,May,Jun",
        "Jul,Aug,Sep",
        "Oct,Nov,Dec"
    ]
    
    # Get the last seven years
    current_year = datetime.now().year
    years = [str(current_year - i) for i in range(7)]
    
    return months, quarters, years

# Example usage
months, quarters, years = get_months_quarters_years()

# # Convert to JSON for embedding in HTML/JavaScript
months_json = json.dumps(months)
#quarters_json = json.dumps(list(quarters.keys()))
quarters_json = json.dumps(quarters)  # No need to list keys; use values directly
years_json = json.dumps(years)

# # Print JSON strings (or send them to your template rendering system)
# print(months_json)
# print(quarters_json)
# print(years_json)


def get_last_seven_years_labels():
    current_year = date.today().year
    return [str(year) for year in range(current_year - 1, current_year - 8, -1)]



from decimal import Decimal, InvalidOperation

def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

def safe_decimal(value):
    if value is None:
        return 0
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError, TypeError):
        return 0
    
#New
    

import logging

logger = logging.getLogger(__name__)

import logging

logger = logging.getLogger(__name__)

import calendar
from datetime import datetime, timedelta

def incomeStatementTable(request, id):
    company = Company.objects.get(company_id=id)

    if request.method == 'POST':
        # Log the old session values
        logger.debug(f"Old session data: {request.session.items()}")

        # Clear old session variables if a new selection is made
        if request.POST.get('select_type_of_data'):
            request.session['income_statement_monthly_date'] = None
            request.session['income_statement_monthly_month_name'] = None
            request.session['income_statement_monthly_end_date'] = None
            request.session['income_statement_quarterly_date'] = None
            request.session['income_statement_quarterly_quarter_value'] = None
            request.session['income_statement_quarterly_end_date'] = None
            request.session['income_statement_yearly_date'] = None
            request.session['income_statement_yearly_year'] = None
            request.session['income_statement_yearly_end_date'] = None
            request.session.modified = True  # Explicitly mark the session as modified

        # Process user input and set new session variables
        select_type_of_data = request.POST.get('select_type_of_data')

        if select_type_of_data == 'monthly':
            year = int(request.POST.get('year'))
            month_name = request.POST.get('month')

            # Convert month name to month number
            month = datetime.strptime(month_name, '%B').month
            date = datetime(year, month, 1)

            # Calculate the last day of the month
            last_day = calendar.monthrange(year, month)[1]
            end_date = datetime(year, month, last_day)

            # Set new session variables
            request.session['income_statement_monthly_date'] = date.strftime('%Y-%m-%d')
            request.session['income_statement_monthly_month_name'] = month_name
            request.session['income_statement_monthly_end_date'] = end_date.strftime('%Y-%m-%d')
            request.session.modified = True  # Force session modification

            # Log the newly set session values
            logger.debug(f"New session data (monthly): {request.session.items()}")

            # Check if income statement for this month already exists
            selected_monthly_income_statement = IncomeStatement.objects.filter(
                company_id=id, date=date, monthly_or_quarterly_or_yearly='monthly'
            )

            if selected_monthly_income_statement:
                messages.error(request, f'Income Statement for {str(year)} {month_name} already exists. Please enter the next month statement.')
                return redirect('planning_budgeting_income_statement_table', id)
            else:
                return redirect('income_statement', id)

        elif select_type_of_data == 'quarterly':
            year = int(request.POST.get('year'))
            quarter = request.POST.get('quarter').split()[0]
            quarter_value = request.POST.get('quarter')

            # Map quarters to starting months and determine the end of the quarter
            quarter_start_months = {
                '0': 1,
                '1': 4,
                '2': 7,
                '3': 10
            }
            month = quarter_start_months[quarter]
            date = datetime(year, month, 1)

            # Calculate the last day of the quarter
            quarter_end_month = month + 2
            last_day = calendar.monthrange(year, quarter_end_month)[1]
            end_date = datetime(year, quarter_end_month, last_day)

            # Set new session variables
            request.session['income_statement_quarterly_date'] = date.strftime('%Y-%m-%d')
            request.session['income_statement_quarterly_quarter_value'] = quarter_value
            request.session['income_statement_quarterly_end_date'] = end_date.strftime('%Y-%m-%d')
            request.session.modified = True  # Force session modification

            # Log the newly set session values
            logger.debug(f"New session data (quarterly): {request.session.items()}")

            # Check if income statement for this quarter already exists
            selected_quarterly_income_statement = IncomeStatement.objects.filter(
                company_id=id, date=date, monthly_or_quarterly_or_yearly='quarterly'
            )

            if selected_quarterly_income_statement:
                messages.error(request, f'Income Statement for {str(year)} {quarter_value} already exists. Please enter the next quarter statement.')
                return redirect('planning_budgeting_income_statement_table', id)
            else:
                return redirect('income_statement', id)

        elif select_type_of_data == 'yearly':
            year = int(request.POST.get('year'))
            date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31)  # The last day of the year

            # Set new session variables
            request.session['income_statement_yearly_date'] = date.strftime('%Y-%m-%d')
            request.session['income_statement_yearly_year'] = year
            request.session['income_statement_yearly_end_date'] = end_date.strftime('%Y-%m-%d')
            request.session.modified = True  # Force session modification

            # Log the newly set session values
            logger.debug(f"New session data (yearly): {request.session.items()}")

            # Check if income statement for this year already exists
            selected_yearly_income_statement = IncomeStatement.objects.filter(
                company_id=id, date=date, monthly_or_quarterly_or_yearly='annually'
            )

            if selected_yearly_income_statement:
                messages.error(request, f'Income Statement for {str(year)} already exists. Please enter the next year statement.')
                return redirect('planning_budgeting_income_statement_table', id)
            else:
                return redirect('income_statement', id)

    else:
        company = Company.objects.get(company_id=id)
        income_statements = IncomeStatement.objects.filter(company_id=id).order_by('-end_date')

        months, quarters, years = get_months_quarters_years()
        incomesheetratios = IncomeStatementRatios.objects.filter(company_id=id).values(
        'incomesheet_id',
        'gross_profit_ratio',
        'operating_profit_ratio',
        'ebitda_margin',
        'net_profit_margin',
        'earnings_per_share',
        'interest_service',
        'operating_cash_flow_ratio',
        'debt_service_coverage_ratio'
    )
        incomesheetratios_list = list(incomesheetratios)
        for ratio in incomesheetratios_list:
            for key, value in ratio.items():
                if isinstance(value, Decimal):
                    ratio[key] = float(value)
        context = {
            'company': company,
            'income_statements': income_statements,
            'months': months,
            'quarters': quarters,
            'years': years,
            'months_json': months_json,
            'quarters_json': quarters_json,
            'years_json': years_json,
             'balancesheetratios_json': json.dumps(list(incomesheetratios_list)),
        }
        return render(request, 'admin/income_statement_table.html', context)





def parse_post_value(value):
    return 0 if value in [None, ''] else value




#New
def incomeStatement(request, id):
    company = Company.objects.get(company_id=id)
    #income_statement = IncomeStatement.objects.filter(company_id=id).last()

    if request.method == 'POST':
      
        # Retrieve and validate POST data
        total_revenue = parse_post_value(request.POST.get('total_revenue'))
        operating_revenue = parse_post_value(request.POST.get('operating_revenue'))
        otherincomeexpense = parse_post_value(request.POST.get('other_income_or_expense'))
        cost_of_revenue = parse_post_value(request.POST.get('cost_of_revenue'))
        gross_profit = parse_post_value(request.POST.get('gross_profit'))
        operatingexpense = parse_post_value(request.POST.get('operating_expense'))
        sellinggeneral = parse_post_value(request.POST.get('selling_general_and_administrative_expense'))
        research_and_development_expense = parse_post_value(request.POST.get('research_and_development_expense'))
        general_and_administrative_expenses = parse_post_value(request.POST.get('general_and_administrative_expenses'))
        selling_and_marketing_expense = parse_post_value(request.POST.get('selling_and_marketing_expense'))
        interest_income_non_operating = parse_post_value(request.POST.get('interest_income_non_operating'))
        interest_expense_non_operating = parse_post_value(request.POST.get('interest_expense_non_operating'))
        gain_or_loss_on_sale_of_security = parse_post_value(request.POST.get('gain_or_loss_on_sale_of_security'))
        special_income_or_charges = parse_post_value(request.POST.get('special_income_or_charges'))
        write_off = parse_post_value(request.POST.get('write_off'))
        operatingincome = parse_post_value(request.POST.get('operating_income'))
        net_non_operating_interest_income_expense = parse_post_value(request.POST.get('net_non_operating_interest_income_expense'))
        other_non_operating_income_or_expenses = parse_post_value(request.POST.get('other_non_operating_income_or_expenses'))
        tax_provision = parse_post_value(request.POST.get('tax_provision'))
        preference_share_dividends = parse_post_value(request.POST.get('preference_share_dividends'))
        equity_share_dividends = parse_post_value(request.POST.get('equity_share_dividends'))
        diluted_eps = parse_post_value(request.POST.get('diluted_eps'))
        depreciation_and_amortization = parse_post_value(request.POST.get('depreciation_and_amortization'))
        no_of_equity_shares = parse_post_value(request.POST.get('no_of_equity_shares'))
        pretax_income = parse_post_value(request.POST.get('pretax_income'))
        net_income = parse_post_value(request.POST.get('net_income'))
        retained_earnings = parse_post_value(request.POST.get('retained_earnings'))
        basic_eps = parse_post_value(request.POST.get('basic_eps'))
        ebitda = parse_post_value(request.POST.get('EBITDA'))
        net_income_to_common_stockholders = parse_post_value(request.POST.get('net_income_to_common_stockholders'))


       


        # Convert to integers if not None, otherwise set to 0
        operating_revenue = float(operating_revenue) if operating_revenue else 0
        cost_of_revenue = float(cost_of_revenue) if cost_of_revenue else 0
        research_and_development_expense = float(research_and_development_expense) if research_and_development_expense else 0
        general_and_administrative_expenses = float(general_and_administrative_expenses) if general_and_administrative_expenses else 0
        selling_and_marketing_expense = float(selling_and_marketing_expense) if selling_and_marketing_expense else 0
        interest_income_non_operating = float(interest_income_non_operating) if interest_income_non_operating else 0
        interest_expense_non_operating = float(interest_expense_non_operating) if interest_expense_non_operating else 0
        gain_or_loss_on_sale_of_security = float(gain_or_loss_on_sale_of_security) if gain_or_loss_on_sale_of_security else 0
        special_income_or_charges = float(special_income_or_charges) if special_income_or_charges else 0
        write_off = float(write_off) if write_off else 0
        other_non_operating_income_or_expenses = float(other_non_operating_income_or_expenses) if other_non_operating_income_or_expenses else 0
        tax_provision = float(tax_provision) if tax_provision else 0
        preference_share_dividends = float(preference_share_dividends) if preference_share_dividends else 0
        equity_share_dividends = float(equity_share_dividends) if equity_share_dividends else 0
        diluted_eps = float(diluted_eps) if diluted_eps else 0
        depreciation_and_amortization = float(depreciation_and_amortization) if depreciation_and_amortization else 0
        no_of_equity_shares = float(no_of_equity_shares) if no_of_equity_shares else 0

        
        monthly_date = request.session.get('income_statement_monthly_date')
        monthly_month_name = request.session.get('income_statement_monthly_month_name')
        quarterly_date = request.session.get('income_statement_quarterly_date')
        quarterly_quarter_value = request.session.get('income_statement_quarterly_quarter_value')
        yearly_date = request.session.get('income_statement_yearly_date')
        yearly_year = request.session.get('income_statement_yearly_year')
        monthly_end_date = request.session.get('income_statement_monthly_end_date')
        yearly_end_date = request.session.get('income_statement_yearly_end_date')
        quarterly_end_date = request.session.get('income_statement_quarterly_end_date')
        

        # Debugging output
        logger.debug(f"Session values received - Monthly: {monthly_date}, Quarterly: {quarterly_quarter_value}, Yearly: {yearly_year}")

        date = None
        monthly_or_quarterly_or_yearly = None
        end_date=None

        # Prioritize based on what is present in the session
        if monthly_date and monthly_month_name:
            date = monthly_date
            monthly_or_quarterly_or_yearly = 'monthly'
            month_or_quarter_or_year_name = monthly_month_name

            end_date=monthly_end_date
        elif quarterly_date and quarterly_quarter_value:
            date = quarterly_date
            end_date=quarterly_end_date
            monthly_or_quarterly_or_yearly = 'quarterly'
            month_or_quarter_or_year_name = quarterly_quarter_value

        elif yearly_date and yearly_year:
            date = yearly_date
            end_date=yearly_end_date
            monthly_or_quarterly_or_yearly = 'Annually'
            month_or_quarter_or_year_name = yearly_year

 
        # If none of the session variables are set, raise an error
        if not date:
            messages.error(request, 'No date or period information found in session. Please select a period again.')
            return redirect('planning_budgeting_income_statement_table', id)

        # Debugging output for selected period
        logger.debug(f"Selected period - Date: {date}, Type: {monthly_or_quarterly_or_yearly}")

        income_statement = IncomeStatement (
            company_id = company,
            date = date,
            end_date=end_date,
            operating_revenue = operating_revenue,
            cost_of_revenue = cost_of_revenue,
            general_and_administrative_expenses = general_and_administrative_expenses,
            selling_and_marketing_expense = selling_and_marketing_expense,
            research_and_development_expense = research_and_development_expense,
            interest_income_non_operating = interest_income_non_operating,
            interest_expense_non_operating = interest_expense_non_operating,
            gain_or_loss_on_sale_of_security = gain_or_loss_on_sale_of_security,
            special_income_or_charges = special_income_or_charges,
            write_off = write_off,
            other_non_operating_income_or_expenses = other_non_operating_income_or_expenses,
            tax_provision = tax_provision,
            preference_share_dividends = preference_share_dividends,
            equity_share_dividends = equity_share_dividends,
            diluted_eps = diluted_eps,
            depreciation_and_amortization = depreciation_and_amortization,
            no_of_equity_shares = no_of_equity_shares,
            total_revenue = total_revenue,
            gross_profit = gross_profit,
            selling_general_and_administrative_expense = sellinggeneral,
            operating_expense = operatingexpense,
            operating_income = operatingincome,
            net_non_operating_interest_income_expense = net_non_operating_interest_income_expense,
            other_income_or_expense = otherincomeexpense,
            pretax_income = pretax_income,
            net_income = net_income,
            net_income_to_common_stockholders = net_income_to_common_stockholders,
            retained_earnings = retained_earnings,
            basic_eps = basic_eps,
            ebitda = ebitda,
            monthly_or_quarterly_or_yearly = monthly_or_quarterly_or_yearly,
            month_or_quarter_or_year_name = month_or_quarter_or_year_name

        )

        # Save income statement
        income_statement.save()
        gross_profit=safe_decimal(safe_int(gross_profit))
        operating_revenue=safe_decimal(safe_int(operating_revenue))
        ebitda=safe_decimal(safe_int(ebitda))
        total_revenue=safe_decimal(safe_int(total_revenue))
        operatingincome=safe_decimal(safe_int(operatingincome))
        net_income_to_common_stockholders=safe_decimal(safe_int(net_income_to_common_stockholders))
        no_of_equity_shares=safe_decimal(safe_int(no_of_equity_shares))
        interest_income_non_operating=safe_decimal(safe_int(interest_income_non_operating))
        net_income=safe_decimal(safe_int(net_income))

        grossprofitratio=gross_profit/operating_revenue if operating_revenue else 0
        operatingprofitratio=operatingincome/operating_revenue if operating_revenue else 0
        ebitdamargin=ebitda/total_revenue if total_revenue else 0
        netprofitmargin=net_income/total_revenue if total_revenue else 0
        earningspershare=net_income_to_common_stockholders/no_of_equity_shares if no_of_equity_shares else 0
        interstservice=operatingincome/interest_income_non_operating if interest_income_non_operating else 0

        incomeratios=IncomeStatementRatios(
            company_id=company,
            incomesheet=income_statement,
            gross_profit_ratio=grossprofitratio,
            operating_profit_ratio=operatingprofitratio,
            ebitda_margin=ebitdamargin,
            net_profit_margin=netprofitmargin,
            earnings_per_share=earningspershare,
            interest_service=interstservice


        )
        incomeratios.save()
        

        return redirect('planning_budgeting_income_statement_table', id)
    else:
        income_statement_monthly_date = request.session.get('income_statement_monthly_date')
        income_statement_monthly_month_name = request.session.get('income_statement_monthly_month_name')
        income_statement_quarterly_quarter_value = request.session.get('income_statement_quarterly_quarter_value')
        income_statement_yearly_year = request.session.get('income_statement_yearly_year')
        income_statement_monthly_end_date = request.session.get('income_statement_monthly_end_date')
        income_statement_yearly_end_date = request.session.get('income_statement_yearly_end_date')
        income_statement_quarterly_end_date = request.session.get('income_statement_quarterly_end_date')
        
        date = None
        

        # Prioritize session values based on user selection
        if income_statement_monthly_date and income_statement_monthly_month_name:
            date = income_statement_monthly_end_date
            period = income_statement_monthly_month_name
        elif income_statement_quarterly_quarter_value:
            date = income_statement_quarterly_end_date
        elif income_statement_yearly_year:
            date = income_statement_yearly_end_date

        context = {
            'company': company,
            'date': date
        }
        

        return render(request, 'admin/income_statement.html', context)

def balanceSheetTable(request, id):
    company = Company.objects.get(company_id=id)

    if request.method == 'POST':
        # Clear old session variables if a new selection is made
        if request.POST.get('select_type_of_data'):
            request.session['balance_sheet_monthly_date'] = None
            request.session['balance_sheet_monthly_end_date'] = None
            request.session['balance_sheet_quarterly_date'] = None
            request.session['balance_sheet_quarterly_end_date'] = None
            request.session['balance_sheet_yearly_date'] = None
            request.session['balance_sheet_yearly_end_date'] = None
            request.session.modified = True  # Mark the session as modified

        # Process user input and set new session variables
        select_type_of_data = request.POST.get('select_type_of_data')

        if select_type_of_data == 'monthly':
            year = int(request.POST.get('year'))
            month_name = request.POST.get('month')

            # Convert month name to month number
            month = datetime.strptime(month_name, '%B').month
            date = datetime(year, month, 1)

            # Calculate the last day of the month
            last_day = calendar.monthrange(year, month)[1]
            end_date = datetime(year, month, last_day)

            # Set session variables for the monthly period
            request.session['balance_sheet_monthly_date'] = date.strftime('%Y-%m-%d')
            request.session['balance_sheet_monthly_end_date'] = end_date.strftime('%Y-%m-%d')
            request.session['balance_sheet_monthly_month_name'] = month_name
            request.session.modified = True

            # Check if the balance sheet for this month already exists
            selected_monthly_balance_sheet = BalanceSheet.objects.filter(
                company_id=id, date=date, monthly_or_quarterly_or_yearly='monthly'
            )

            if selected_monthly_balance_sheet:
                messages.error(request, f'Balance Sheet for {str(year)} {month_name} already exists. Please enter the next month.')
                return redirect('planning_budgeting_balance_sheet_table', id)
            else:
                return redirect('balance_sheet', id)

        elif select_type_of_data == 'quarterly':
            year = int(request.POST.get('year'))
            quarter_value = request.POST.get('quarter').split()[0]
           


            quarter_start_months = {
                '0': 1,
                '1': 4,
                '2': 7,
                '3': 10
            }
            start_month = quarter_start_months[quarter_value]
            date = datetime(year, start_month, 1)

            end_month = start_month + 2
            last_day = calendar.monthrange(year, end_month)[1]
            end_date = datetime(year, end_month, last_day)

            
            request.session['balance_sheet_quarterly_date'] = date.strftime('%Y-%m-%d')
            request.session['balance_sheet_quarterly_end_date'] = end_date.strftime('%Y-%m-%d')
            request.session['balance_sheet_quarterly_quarter_value'] = quarter_value
            request.session.modified = True

            
            selected_quarterly_balance_sheet = BalanceSheet.objects.filter(
                company_id=id, date=date, monthly_or_quarterly_or_yearly='quarterly'
            )

            if selected_quarterly_balance_sheet:
                messages.error(request, f'Balance Sheet for {str(year)} {quarter_value} already exists. Please enter the next quarter.')
                return redirect('planning_budgeting_balance_sheet_table', id)
            else:
                return redirect('balance_sheet', id)

        elif select_type_of_data == 'yearly':
            year = int(request.POST.get('year'))

            # Set start and end dates for the year
            date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31)

            # Set session variables for the yearly period
            request.session['balance_sheet_yearly_date'] = date.strftime('%Y-%m-%d')
            request.session['balance_sheet_yearly_end_date'] = end_date.strftime('%Y-%m-%d')
            request.session['balance_sheet_yearly_year'] = 'annually'
            request.session.modified = True

            # Check if the balance sheet for this year already exists
            selected_yearly_balance_sheet = BalanceSheet.objects.filter(
                company_id=id, date=date, monthly_or_quarterly_or_yearly=year
            )

            if selected_yearly_balance_sheet:
                messages.error(request, f'Balance Sheet for {str(year)} already exists. Please enter the next year.')
                return redirect('planning_budgeting_balance_sheet_table', id)
            else:
                return redirect('balance_sheet', id)

    else:
        company = Company.objects.get(company_id=id)
        balance_sheets = BalanceSheet.objects.filter(company_id=id).order_by('-end_date')
        months, quarters, years = get_months_quarters_years()
        balancesheetratios = BalanceSheetRatios.objects.filter(company_id=id).values(
        'balancesheet_id',
        'current_ratio',
        'quick_ratio',
        'cash_ratio',
        'working_capital',
        'debt_equity_ratio',
        'debt_ratio',
        'equity_ratio',
        'debt_capital_ratio',
        'operating_cash_flow_ratio',
        'debt_service_coverage_ratio'
        )

    # Convert Decimal fields to float or string
        balancesheetratios_list = list(balancesheetratios)
        for ratio in balancesheetratios_list:
            for key, value in ratio.items():
                if isinstance(value, Decimal):
                    ratio[key] = float(value) 
        context = {
            'company': company,
            'balance_sheets': balance_sheets,
            'months': months,
            'quarters': quarters,
            'years': years,
            'months_json': months_json,
            'quarters_json': quarters_json,
            'years_json': years_json,
            'balancesheetratios_json': json.dumps(list(balancesheetratios_list)),
        }
        return render(request, 'admin/balance_sheet_table.html', context)







#New   
def balanceSheet(request, id):
    company = Company.objects.get(company_id=id)
    #balance_sheet = BalanceSheet.objects.filter(company_id=id).last()


    if request.method == 'POST':

        cash = parse_post_value(request.POST.get('cash'))
        cash_equivalents = parse_post_value(request.POST.get('cash_equivalents'))
        other_short_term_investments = parse_post_value(request.POST.get('short_term_investments'))
        gross_accounts_receivable = parse_post_value(request.POST.get('grossAccountsReceivable'))
        allowance_for_doubtful_accounts_receivable = parse_post_value(request.POST.get('allowanceForDoubtful'))
        other_receivables = parse_post_value(request.POST.get('otherReceivables'))
        raw_materials = parse_post_value(request.POST.get('rawMaterials'))
        work_in_process = parse_post_value(request.POST.get('workInProcess'))
        finished_goods = parse_post_value(request.POST.get('finishedGoods'))
        hedging_current_assets = parse_post_value(request.POST.get('hedgingAssetsCurrent'))
        other_current_assets = parse_post_value(request.POST.get('otherCurrentAssets'))
        land_and_improvements = parse_post_value(request.POST.get('land_and_improvements'))
        buildings_and_improvements = parse_post_value(request.POST.get('buildings_and_improvements'))
        machinery_furniture_equipment = parse_post_value(request.POST.get('machinery_furniture_equipment'))
        other_properties = parse_post_value(request.POST.get('other_properties'))
        leases = parse_post_value(request.POST.get('leases'))
        accumulated_depreciation = parse_post_value(request.POST.get('accumulated_depreciation'))
        goodwill = parse_post_value(request.POST.get('goodwill'))
        other_intangible_assets = parse_post_value(request.POST.get('other_intangible_assets'))
        long_term_equity_investment = parse_post_value(request.POST.get('long_term_equity_investment'))
        other_non_current_assets = parse_post_value(request.POST.get('other_non_current_assets'))
        accounts_payable = parse_post_value(request.POST.get('accounts_payable'))
        income_tax_payable = parse_post_value(request.POST.get('income_tax_payable'))
        pension_and_other_post_retirement_benefit_plans_current = parse_post_value(request.POST.get('pension_and_other_post_retirement_benefit_plans_current'))
        current_debt = parse_post_value(request.POST.get('current_debt'))
        capital_lease_obligation = parse_post_value(request.POST.get('capital_lease_obligation'))
        current_deferred_revenue = parse_post_value(request.POST.get('current_deferred_revenue'))
        other_current_liabilities = parse_post_value(request.POST.get('other_current_liabilities'))
        long_term_debt = parse_post_value(request.POST.get('long_term_debt'))
        long_term_capital_lease_obligation = parse_post_value(request.POST.get('long_term_capital_lease_obligation'))
        non_current_deferred_taxes_liabilities = parse_post_value(request.POST.get('non_current_deferred_taxes_liabilities'))
        non_current_deferred_revenue = parse_post_value(request.POST.get('non_current_deferred_revenue'))
        trade_and_other_payables_non_current = parse_post_value(request.POST.get('trade_and_other_payables_non_current'))
        other_non_current_liabilities = parse_post_value(request.POST.get('other_non_current_liabilities'))
        common_stock = parse_post_value(request.POST.get('common_stock'))
        retained_earnings = parse_post_value(request.POST.get('retained_earnings'))
        gains_or_losses_not_affecting_retained_earnings = parse_post_value(request.POST.get('gains_or_losses_not_affecting_retained_earnings'))
        other_equity_adjustments = parse_post_value(request.POST.get('other_equity_adjustments'))
        cash_and_cash_equivalents = parse_post_value(request.POST.get('cashAndCashEquivalents'))
        total_assets = parse_post_value(request.POST.get('totalAssets'))
        current_assets = parse_post_value(request.POST.get('currentAssets'))
        cash_cash_equivalents_and_short_term_investments = parse_post_value(request.POST.get('cashEquivalentsShotTerm'))
        receivables = parse_post_value(request.POST.get('receivables'))
        accounts_receivable = parse_post_value(request.POST.get('accountsReceivable'))
        inventory = parse_post_value(request.POST.get('inventory'))
        total_non_current_assets = parse_post_value(request.POST.get('totalNon_CurrentAssets'))
        net_ppe = parse_post_value(request.POST.get('netPPE'))
        gross_ppe = parse_post_value(request.POST.get('grossPPE'))
        goodwill_and_other_intangible_assets = parse_post_value(request.POST.get('goodwillAssets'))
        investments_and_advances = parse_post_value(request.POST.get('investAdvance'))
        total_liabilities_net_minority_interest = parse_post_value(request.POST.get('total_Liabilities_net'))
        current_liabilities = parse_post_value(request.POST.get('current_Liabilities'))
        payables_and_accrued_expenses = parse_post_value(request.POST.get('payables_Accrued'))
        current_debt_and_capital_lease_obligation = parse_post_value(request.POST.get('current_debt_and_Capital_lease'))
        current_deferred_liabilities = parse_post_value(request.POST.get('current_deferred_liabilities'))
        total_non_current_liabilities_net_minority_interest = parse_post_value(request.POST.get('total_non_current_liabilities_net_minority'))
        long_term_debt_and_capital_lease_obligation = parse_post_value(request.POST.get('long_term_debt_and_capital_lease_obligation'))
        non_current_deferred_liabilities = parse_post_value(request.POST.get('non_current_deferred_liabilities'))
        total_equity_gross_minority_interest = parse_post_value(request.POST.get('total_equity_gross_minority_interest'))
        stockholders_equity = parse_post_value(request.POST.get('stockholders_equity'))
        capital_stock = parse_post_value(request.POST.get('capital_stock'))
       
        
        

        # Ensure income_statement is not None
        # if income_statement is None:
        #     income_statement = IncomeStatement(company_id=id)

        balance_sheet_monthly_date  = request.session.get('balance_sheet_monthly_date') 
        balance_sheet_monthly_month_name = request.session.get('balance_sheet_monthly_month_name')
        balance_sheet_quarterly_date  = request.session.get('balance_sheet_quarterly_date') 
        balance_sheet_quarterly_quarter_value = request.session.get('balance_sheet_quarterly_quarter_value')
        balance_sheet_yearly_date  = request.session.get('balance_sheet_yearly_date') 
        balance_sheet_yearly_year  = request.session.get('balance_sheet_yearly_year')
        quarterly_end_date = request.session.get('balance_sheet_quarterly_end_date')
        yearly_end_date = request.session.get('balance_sheet_yearly_end_date')
        monthly_end_date = request.session.get('balance_sheet_monthly_end_date')
        date=None
        end_date=None
        monthly_or_quarterly_or_yearly=None

        if balance_sheet_monthly_date and balance_sheet_monthly_month_name:
            date = balance_sheet_monthly_date
            monthly_or_quarterly_or_yearly = 'monthly'
            month_or_quarter_or_year_name = balance_sheet_monthly_month_name
            end_date=monthly_end_date
        if balance_sheet_quarterly_date and balance_sheet_quarterly_quarter_value:
            date = balance_sheet_quarterly_date
            monthly_or_quarterly_or_yearly = 'quarterly'
            month_or_quarter_or_year_name = balance_sheet_quarterly_quarter_value

            end_date=quarterly_end_date
        if balance_sheet_yearly_date and balance_sheet_yearly_year:
            date = balance_sheet_yearly_date
            monthly_or_quarterly_or_yearly = 'Annually'
            month_or_quarter_or_year_name = balance_sheet_yearly_year

            end_date=yearly_end_date
        
       

        
        
        balance_sheet = BalanceSheet(
            company_id = company,
            date = date,
            end_date=end_date,
            cash = cash,
            cash_equivalents = cash_equivalents,
            other_short_term_investments = other_short_term_investments,
            gross_accounts_receivable = gross_accounts_receivable,
            allowance_for_doubtful_accounts_receivable = allowance_for_doubtful_accounts_receivable,
            other_receivables = other_receivables,
            raw_materials = raw_materials,
            work_in_process = work_in_process,
            finished_goods = finished_goods,
            hedging_current_assets = hedging_current_assets,
            other_current_assets = other_current_assets,
            land_and_improvements = land_and_improvements,
            buildings_and_improvements = buildings_and_improvements,
            machinery_furniture_equipment = machinery_furniture_equipment,
            other_properties = other_properties,
            leases = leases,
            accumulated_depreciation = accumulated_depreciation,
            goodwill = goodwill,
            other_intangible_assets = other_intangible_assets,
            long_term_equity_investment = long_term_equity_investment,
            other_non_current_assets = other_non_current_assets,
            accounts_payable = accounts_payable,
            income_tax_payable = income_tax_payable,
            pension_and_other_post_retirement_benefit_plans_current = pension_and_other_post_retirement_benefit_plans_current,
            current_debt = current_debt,
            capital_lease_obligation = capital_lease_obligation,
            current_deferred_revenue = current_deferred_revenue,
            other_current_liabilities = other_current_liabilities,
            long_term_debt = long_term_debt,
            long_term_capital_lease_obligation = long_term_capital_lease_obligation,
            non_current_deferred_taxes_liabilities = non_current_deferred_taxes_liabilities,
            non_current_deferred_revenue = non_current_deferred_revenue,
            trade_and_other_payables_non_current = trade_and_other_payables_non_current,
            other_non_current_liabilities = other_non_current_liabilities,
            common_stock = common_stock,
            retained_earnings = retained_earnings,
            gains_or_losses_not_affecting_retained_earnings = gains_or_losses_not_affecting_retained_earnings,
            other_equity_adjustments = other_equity_adjustments,
            cash_and_cash_equivalents = cash_and_cash_equivalents,
            inventory = inventory,
            capital_stock = capital_stock,
            cash_cash_equivalents_and_short_term_investments = cash_cash_equivalents_and_short_term_investments,
            accounts_receivable = accounts_receivable,
            receivables = receivables,
            current_assets = current_assets,
            gross_ppe = gross_ppe,
            net_ppe = net_ppe,
            goodwill_and_other_intangible_assets = goodwill_and_other_intangible_assets,
            investments_and_advances = investments_and_advances,
            total_non_current_assets = total_non_current_assets,
            total_assets = total_assets,
            payables_and_accrued_expenses = payables_and_accrued_expenses,
            current_debt_and_capital_lease_obligation = current_debt_and_capital_lease_obligation,
            current_deferred_liabilities = current_deferred_liabilities,
            current_liabilities = current_liabilities,
            long_term_debt_and_capital_lease_obligation = long_term_debt_and_capital_lease_obligation,
            non_current_deferred_liabilities = non_current_deferred_liabilities,
            total_non_current_liabilities_net_minority_interest = total_non_current_liabilities_net_minority_interest,
            total_liabilities_net_minority_interest = total_liabilities_net_minority_interest,
            stockholders_equity = stockholders_equity,
            total_equity_gross_minority_interest = total_equity_gross_minority_interest,
            monthly_or_quarterly_or_yearly = monthly_or_quarterly_or_yearly,
            month_or_quarter_or_year_name = month_or_quarter_or_year_name
  

        )
        balance_sheet.save()
        current_assets=request.POST.get('current_assets')

        current_assets = safe_decimal(safe_int(current_assets))
        current_liabilities = safe_decimal(safe_int(current_liabilities))
        cash_and_cash_equivalents = safe_decimal(safe_int(cash_and_cash_equivalents))
        other_non_current_liabilities = safe_decimal(safe_int(other_non_current_liabilities))
        stockholders_equity = safe_decimal(safe_int(stockholders_equity))
        total_assets = safe_decimal(safe_int(total_assets))
        inventory = safe_decimal(safe_int(inventory))

        current_ratio = current_assets / current_liabilities if current_liabilities else 0
        quick_ratio = (current_assets - inventory) / current_liabilities if current_liabilities else 0
        cash_ratio = cash_and_cash_equivalents / current_liabilities if current_liabilities else 0
        working_capital = current_assets - current_liabilities
        debt_equity_ratio = other_non_current_liabilities / stockholders_equity if stockholders_equity else 0
        debt_ratio = other_non_current_liabilities / total_assets if total_assets else 0
        equity_ratio = stockholders_equity / total_assets if total_assets else 0
        debt_capital_ratio = other_non_current_liabilities / (stockholders_equity + other_non_current_liabilities) if (stockholders_equity + other_non_current_liabilities) else 0
        
        
        balance_sheet_ratios = BalanceSheetRatios(
        company_id=company,
        balancesheet=balance_sheet,
        current_ratio=current_ratio,
        quick_ratio=quick_ratio,
        cash_ratio=cash_ratio,
        working_capital=working_capital,
        debt_equity_ratio=debt_equity_ratio,
        debt_ratio=debt_ratio,
        equity_ratio=equity_ratio,
        debt_capital_ratio=debt_capital_ratio,
        # Assuming you have values for these ratios, if not, set them accordingly
        
         )

        balance_sheet_ratios.save()


        return redirect('planning_budgeting_balance_sheet_table', id)
    else:
        balance_sheet_monthly_date = request.session.get('balance_sheet_monthly_date')
        balance_sheet_monthly_end_date = request.session.get('balance_sheet_monthly_end_date')
        balance_sheet_monthly_month_name = request.session.get('balance_sheet_monthly_month_name')
        balance_sheet_quarterly_quarter_value = request.session.get('balance_sheet_quarterly_quarter_value')
        balance_sheet_yearly_year = request.session.get('balance_sheet_yearly_year')
        balance_sheet_quarterly_end_date = request.session.get('balance_sheet_quarterly_end_date')
        balance_sheet_yearly_end_date = request.session.get('balance_sheet_yearly_end_date')

        period=None
        date = None
        if balance_sheet_monthly_date and balance_sheet_monthly_month_name:
            date = balance_sheet_monthly_end_date
            period="monthly"
        elif balance_sheet_quarterly_quarter_value:
            date = balance_sheet_quarterly_end_date
            period=balance_sheet_quarterly_quarter_value
        elif balance_sheet_yearly_year:
            date = balance_sheet_yearly_end_date
            period=balance_sheet_yearly_year

        incomestatement = IncomeStatement.objects.filter(
            company_id=id,
            monthly_or_quarterly_or_yearly=period,
            end_date__lte=date  # Use __gt to compare end_date greater than the provided date
        )

        print(incomestatement)
        retained_earnings=0
        for i in incomestatement:
            retained_earnings+=i.retained_earnings
    
        
        context = {
            'company': company,
            'date': date,
            'retained_earnings':retained_earnings
        }

        return render(request, 'admin/balance_sheet.html', context)





def check_previous_entry_exists_old(date, company, period_type):
    # Calculate the previous period based on the type
    if period_type == 'monthly':
        # First day of the previous month
        previous_month = date.replace(day=1) - timedelta(days=1)
        previous_period_date = previous_month.replace(day=1)
    elif period_type == 'quarterly':
        # Calculate the start month of the previous quarter
        previous_quarter_start_month = ((date.month - 1) // 3 * 3) - 3
        if previous_quarter_start_month < 1:
            previous_quarter_start_month = 10
            year = date.year - 1
        else:
            year = date.year
        previous_period_date = datetime(year, previous_quarter_start_month, 1)
    elif period_type == 'yearly':
        # Start of the previous year
        previous_period_date = datetime(date.year - 1, 1, 1)

    # Retrieve the previous period BalanceSheet and IncomeStatement
    previous_balance_sheet = BalanceSheet.objects.filter(company_id=company, date=previous_period_date).first()
    previous_income_statement = IncomeStatement.objects.filter(company_id=company, date=previous_period_date).first()
    
    # Check if the previous period exists in BalanceSheet and IncomeStatement
    period_exists = previous_balance_sheet and previous_income_statement
    
    return period_exists, previous_period_date, previous_balance_sheet, previous_income_statement




from datetime import datetime, timedelta

def check_previous_entry_exists(date, company, period_type):
    # Convert string to datetime object if needed
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')  # Assuming date is in 'YYYY-MM-DD' format

    # Calculate the previous period based on the type
    if period_type == 'monthly':
        # First day of the previous month
        previous_month = date.replace(day=1) - timedelta(days=1)
        previous_period_date = previous_month.replace(day=1)
    elif period_type == 'quarterly':
        # Calculate the start month of the previous quarter
        previous_quarter_start_month = ((date.month - 1) // 3 * 3) - 3
        if previous_quarter_start_month < 1:
            previous_quarter_start_month = 10
            year = date.year - 1
        else:
            year = date.year
        previous_period_date = datetime(year, previous_quarter_start_month, 1)
    elif period_type == 'yearly':
        # Start of the previous year
        previous_period_date = datetime(date.year - 1, 1, 1)

    # Retrieve the previous period BalanceSheet and IncomeStatement
    previous_balance_sheet = BalanceSheet.objects.filter(company_id=company, date=previous_period_date).first()
    previous_income_statement = IncomeStatement.objects.filter(company_id=company, date=previous_period_date).first()
    
    # Check if the previous period exists in BalanceSheet and IncomeStatement
    period_exists = previous_balance_sheet and previous_income_statement
    
    return period_exists, previous_period_date, previous_balance_sheet, previous_income_statement

def get_balance_sheet_and_income_statement(date, company):
    balance_sheet = BalanceSheet.objects.filter(company_id=company, date=date).first()
    income_statement = IncomeStatement.objects.filter(company_id=company, date=date).first()
    return balance_sheet, income_statement

from datetime import datetime, timedelta

def get_next_period_data(date, company, period_type):
    if period_type == 'monthly':
        # Calculate the first day of the next month
        next_period = (date.replace(day=1) + timedelta(days=32)).replace(day=1)
        
    elif period_type == 'quarterly':
        # Calculate the start month of the next quarter
        next_quarter_start_month = ((date.month - 1) // 3 * 3) + 3
        if next_quarter_start_month > 12:
            next_quarter_start_month = 1
            next_year = date.year + 1
        else:
            next_year = date.year
        next_period = datetime(next_year, next_quarter_start_month, 1)

    elif period_type == 'yearly':
        # Start of the next year
        next_period = datetime(date.year + 1, 1, 1)

    # Retrieve the next period BalanceSheet and IncomeStatement
    next_balance_sheet = BalanceSheet.objects.filter(company_id=company, date=next_period).first()
    next_income_statement = IncomeStatement.objects.filter(company_id=company, date=next_period).first()

    # Check if the next period exists in BalanceSheet and IncomeStatement
    next_period_exists = next_balance_sheet and next_income_statement
    
    return next_period_exists, next_period, next_balance_sheet, next_income_statement



def calculate_cash_flow(current_balance_sheet, current_income_statement, previous_balance_sheet, previous_income_statement):
    print(previous_balance_sheet, previous_income_statement, current_balance_sheet, current_income_statement)
    net_income_from_continuing_operations = float(current_income_statement.net_income) 
    depreciation_and_amortization = float(current_income_statement.depreciation_and_amortization)
    changes_in_receivables = float(previous_balance_sheet.receivables) - float(current_balance_sheet.receivables)
    
    change_in_inventory = float(previous_balance_sheet.inventory) - float(current_balance_sheet.inventory)
    change_in_hedging_assets_current = float(previous_balance_sheet.hedging_current_assets) - float(current_balance_sheet.hedging_current_assets)
    change_in_other_current_assets = float(previous_balance_sheet.other_current_assets) - float(current_balance_sheet.other_current_assets)
    change_in_payables_and_accrued_expense =  float(current_balance_sheet.payables_and_accrued_expenses) - float(previous_balance_sheet.payables_and_accrued_expenses)
    change_in_pension_and_other_post_retirement_benefit_plans_current = float(current_balance_sheet.pension_and_other_post_retirement_benefit_plans_current) - float(previous_balance_sheet.pension_and_other_post_retirement_benefit_plans_current)
    change_in_current_debt_and_capital_lease_obligation = float(current_balance_sheet.current_debt_and_capital_lease_obligation) - float(previous_balance_sheet.current_debt_and_capital_lease_obligation)
    change_in_current_deferred_liabilities = float(current_balance_sheet.current_deferred_liabilities) - float(previous_balance_sheet.current_deferred_liabilities)
    change_in_other_current_liabilities = float(current_balance_sheet.other_current_liabilities) - float(previous_balance_sheet.other_current_liabilities)
    change_in_working_capital = ( changes_in_receivables + change_in_inventory + change_in_hedging_assets_current + change_in_other_current_assets + change_in_payables_and_accrued_expense + 
    change_in_pension_and_other_post_retirement_benefit_plans_current + change_in_current_debt_and_capital_lease_obligation + change_in_current_deferred_liabilities + change_in_other_current_liabilities )
    operating_cash_flow = net_income_from_continuing_operations + depreciation_and_amortization + change_in_working_capital
    net_ppe_purchase_and_sale = float(previous_balance_sheet.gross_ppe) - float(current_balance_sheet.gross_ppe)
    #print(net_ppe_purchase_and_sale,'net_ppe_purchase_and_sale')
    goodwill_and_other_intangible_assets = float(previous_balance_sheet.goodwill_and_other_intangible_assets) - float(current_balance_sheet.goodwill_and_other_intangible_assets)
    investments_and_advances = float(previous_balance_sheet.investments_and_advances) - float(current_balance_sheet.investments_and_advances)
    other_non_current_assets = float(previous_balance_sheet.other_non_current_assets) - float(current_balance_sheet.other_non_current_assets)
    cash_flow_from_continuing_investing_activities = ( net_ppe_purchase_and_sale + goodwill_and_other_intangible_assets + investments_and_advances +  other_non_current_assets )
    investing_cash_flow = cash_flow_from_continuing_investing_activities
    long_term_debt_and_capital_lease_obligation = float(current_balance_sheet.long_term_capital_lease_obligation) - float(previous_balance_sheet.long_term_capital_lease_obligation)
    non_current_deferred_liabilities = float(current_balance_sheet.non_current_deferred_liabilities) - float(previous_balance_sheet.non_current_deferred_liabilities)
    trade_and_other_payables_non_current = float(current_balance_sheet.trade_and_other_payables_non_current) - float(previous_balance_sheet.trade_and_other_payables_non_current)
    other_non_current_liabilities = float(current_balance_sheet.other_non_current_liabilities) - float(previous_balance_sheet.other_non_current_liabilities)
    common_stock_issuance_payments = (float(current_balance_sheet.common_stock) + float(current_balance_sheet.gains_or_losses_not_affecting_retained_earnings) + float(current_balance_sheet.other_equity_adjustments)) -(float(previous_balance_sheet.common_stock) + float(previous_balance_sheet.gains_or_losses_not_affecting_retained_earnings) + float(previous_balance_sheet.other_equity_adjustments))
    common_stock_dividend_paid = float(current_income_statement.equity_share_dividends)
    cash_flow_from_continuing_financing_activities = ( long_term_debt_and_capital_lease_obligation +  non_current_deferred_liabilities + trade_and_other_payables_non_current + other_non_current_liabilities +
                                                       common_stock_issuance_payments + common_stock_dividend_paid )
    financing_cash_flow = cash_flow_from_continuing_financing_activities
    changes_in_cash = operating_cash_flow + investing_cash_flow + financing_cash_flow
    beginning_cash_position = float(previous_balance_sheet.cash_cash_equivalents_and_short_term_investments)
    end_cash_position = changes_in_cash + beginning_cash_position
    capital_expenditure = net_ppe_purchase_and_sale 
    issuance_repurchase_of_capital_stock = common_stock_issuance_payments
    repayment_of_debt = long_term_debt_and_capital_lease_obligation 
    free_cash_flow = end_cash_position + capital_expenditure + issuance_repurchase_of_capital_stock + repayment_of_debt

    return {
        'net_income_from_continuing_operations': net_income_from_continuing_operations,
        'depreciation_and_amortization': depreciation_and_amortization,
        'changes_in_receivables': changes_in_receivables,
        'change_in_inventory': change_in_inventory,
        'change_in_hedging_assets_current': change_in_hedging_assets_current,
        'change_in_other_current_assets': change_in_other_current_assets,
        'change_in_payables_and_accrued_expense': change_in_payables_and_accrued_expense,
        'change_in_pension_and_other_post_retirement_benefit_plans_current': change_in_pension_and_other_post_retirement_benefit_plans_current,
        'change_in_current_debt_and_capital_lease_obligation': change_in_current_debt_and_capital_lease_obligation,
        'change_in_current_deferred_liabilities': change_in_current_deferred_liabilities,
        'change_in_other_current_liabilities': change_in_other_current_liabilities,
        'change_in_working_capital': change_in_working_capital,
        'operating_cash_flow': operating_cash_flow,
        'net_ppe_purchase_and_sale': net_ppe_purchase_and_sale,
        'goodwill_and_other_intangible_assets': goodwill_and_other_intangible_assets,
        'investments_and_advances': investments_and_advances,
        'other_non_current_assets': other_non_current_assets,
        'cash_flow_from_continuing_investing_activities': cash_flow_from_continuing_investing_activities,
        'investing_cash_flow': investing_cash_flow,
        'long_term_debt_and_capital_lease_obligation': long_term_debt_and_capital_lease_obligation,
        'non_current_deferred_liabilities': non_current_deferred_liabilities,
        'trade_and_other_payables_non_current': trade_and_other_payables_non_current,
        'other_non_current_liabilities': other_non_current_liabilities,
        'common_stock_issuance_payments': common_stock_issuance_payments,
        'common_stock_dividend_paid': common_stock_dividend_paid,
        'cash_flow_from_continuing_financing_activities': cash_flow_from_continuing_financing_activities,
        'financing_cash_flow': financing_cash_flow,
        'changes_in_cash': changes_in_cash,
        'beginning_cash_position': beginning_cash_position,
        'end_cash_position': end_cash_position,
        'capital_expenditure': capital_expenditure,
        'issuance_repurchase_of_capital_stock': issuance_repurchase_of_capital_stock,
        'repayment_of_debt': repayment_of_debt,
        'free_cash_flow': free_cash_flow,
        'monthly_or_quarterly_or_yearly': current_balance_sheet.monthly_or_quarterly_or_yearly
    }

def cashFlowTable(request, id):
    company = Company.objects.get(company_id=id)
    cash_flows = CashFlow.objects.filter(company_id=id)
    months, quarters, years = get_months_quarters_years()
    cashratio = CashFlowRatios.objects.filter(company_id=id).values(
        'cashflowsheet_id',
        'current_ratio',
        'quick_ratio',
        'cash_ratio',
        'working_capital',
        'operating_cash_flow_ratio',
        'debt_service_coverage_ratio'
    )
    cashratio_list = list(cashratio)

    for ratio in cashratio_list:
        for key, value in ratio.items():
            if isinstance(value, Decimal):
                ratio[key] = float(value) 
    # Initialize the context for both GET and POST

    context = {
    'company': company,
    'cash_flows': cash_flows,
    'months': months,
    'quarters': quarters,
    'years': years,
    'months_json': months_json,
    'quarters_json': quarters_json,
    'years_json': years_json,
    'cashratio_json': json.dumps(cashratio_list),  # Correct key and value
}


    if request.method == 'POST':
        select_type_of_data = request.POST.get('select_type_of_data')
        first_period = request.POST.get('first_period', None)
        date = None
        end_date = None
        
        if select_type_of_data == 'monthly':
            year = int(request.POST.get('year'))
            month_name = request.POST.get('month')
            month = datetime.strptime(month_name, '%B').month
            date = datetime(year, month, 1)

            # Calculate end date for the month
            last_day = calendar.monthrange(year, month)[1]
            end_date = datetime(year, month, last_day)

            # Set session values for monthly
            request.session['cash_flow_monthly_date'] = date.strftime('%Y-%m-%d')
            request.session['cash_flow_monthly_end_date'] = end_date.strftime('%Y-%m-%d')
            request.session['cash_flow_monthly_month_name'] = month_name

        elif select_type_of_data == 'quarterly':
            year = int(request.POST.get('year'))
            quarter = request.POST.get('quarter').split()[0]
            quarter_value = request.POST.get('quarter')
            quarter_start_months = {'0': 1, '1': 4, '2': 7, '3': 10}
            month = quarter_start_months[quarter]
            date = datetime(year, month, 1)

            # Calculate end date for the quarter (last day of the third month in the quarter)
            end_month = month + 2
            last_day = calendar.monthrange(year, end_month)[1]
            end_date = datetime(year, end_month, last_day)

            # Set session values for quarterly
            request.session['cash_flow_quarterly_date'] = date.strftime('%Y-%m-%d')
            request.session['cash_flow_quarterly_end_date'] = end_date.strftime('%Y-%m-%d')
            request.session['cash_flow_quarterly_quarter_value'] = quarter_value

        elif select_type_of_data == 'yearly':
            year = int(request.POST.get('year'))
            date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31)

            # Set session values for yearly
            request.session['cash_flow_yearly_date'] = date.strftime('%Y-%m-%d')
            request.session['cash_flow_yearly_end_date'] = end_date.strftime('%Y-%m-%d')
            request.session['cash_flow_yearly_year'] = year

        period_type = select_type_of_data
        period_exists, previous_period_date, previous_balance_sheet, previous_income_statement = check_previous_entry_exists(date, id, period_type)
        current_balance_sheet, current_income_statement = get_balance_sheet_and_income_statement(date, id)

        if first_period == 'yes':
            return redirect('cashflowfirstyearofoperations', id=id)
        
        elif not current_balance_sheet or not current_income_statement:
            context['manual_entry_option'] = True  # Control for showing buttons
            context['missing_data'] = 'current'  # Missing current period data
        elif not period_exists:
            context['manual_entry_option'] = True  # Control for showing buttons
            context['missing_data'] = 'previous'  # Missing previous period data
        else:
            cash_flow_data = calculate_cash_flow(current_balance_sheet, current_income_statement, previous_balance_sheet, previous_income_statement)
            cash_flow = CashFlow(
                company_id=company,
                date=date,
                end_date=end_date,
                **cash_flow_data,
                month_or_quarter_or_year_name = month_name if select_type_of_data == 'monthly' else (quarter_value if select_type_of_data == 'quarterly' else year)
            )
            cash_flow.save()
            #cash_flow=CashFlow.objects.get(company_id=id, date=date)
            cash_flow_ratios = CashFlowRatios(
            company_id=company,
            cashflowsheet=cash_flow,
            current_ratio=(safe_decimal1(current_balance_sheet.current_assets) / safe_decimal1(current_balance_sheet.current_liabilities)) if current_balance_sheet.current_liabilities else Decimal(0),
            quick_ratio=((safe_decimal1(current_balance_sheet.current_assets) - safe_decimal1(current_balance_sheet.inventory)) / safe_decimal1(current_balance_sheet.current_liabilities)) if current_balance_sheet.current_liabilities else Decimal(0),
            cash_ratio=(safe_decimal1(current_balance_sheet.cash_and_cash_equivalents) / safe_decimal1(current_balance_sheet.current_liabilities)) if current_balance_sheet.current_liabilities else Decimal(0),
            working_capital=(safe_decimal1(current_balance_sheet.current_assets) - safe_decimal1(current_balance_sheet.current_liabilities)),
            operating_cash_flow_ratio=(safe_decimal1(cash_flow.operating_cash_flow) / safe_decimal1(current_balance_sheet.current_liabilities)) if current_balance_sheet.current_liabilities else Decimal(0),
            debt_service_coverage_ratio=(safe_decimal1(current_income_statement.operating_income) / safe_decimal1(current_balance_sheet.other_non_current_liabilities)) if current_balance_sheet.other_non_current_liabilities else Decimal(0)
            )
            cash_flow_ratios.save()
            return redirect('planning_budgeting_cash_flow_table', id)

    return render(request, 'admin/cash_flow_table.html', context)
from decimal import Decimal, InvalidOperation

def safe_decimal1(value):
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError, TypeError):
        logger.error(f"Invalid value for Decimal conversion: {value}")
        return Decimal(0)

def cashflowmanualentry(request, id):
    if request.method == 'POST':
        company = Company.objects.get(company_id=id)
        cash_flow_monthly_date = request.session.get('cash_flow_monthly_date')
        cash_flow_monthly_end_date = request.session.get('cash_flow_monthly_end_date')
        cash_flow_monthly_month_name = request.session.get('cash_flow_monthly_month_name')
        cash_flow_quarterly_date = request.session.get('cash_flow_quarterly_date')
        cash_flow_quarterly_quarter_value = request.session.get('cash_flow_quarterly_quarter_value')
        cash_flow_yearly_date = request.session.get('cash_flow_yearly_date')
        cash_flow_yearly_year = request.session.get('cash_flow_yearly_year')
        cash_flow_yearly_end_date = request.session.get('cash_flow_yearly_end_date')
        cash_flow_quarterly_end_date = request.session.get('cash_flow_quarterly_end_date')

        date=None
        monthly_or_quarterly_or_yearly=None
        end_date=None

        if cash_flow_monthly_date and cash_flow_monthly_month_name:
            date = cash_flow_monthly_date
            monthly_or_quarterly_or_yearly = cash_flow_monthly_month_name
            end_date=cash_flow_monthly_end_date
        if cash_flow_quarterly_date and cash_flow_quarterly_quarter_value:
            date = cash_flow_quarterly_date
            monthly_or_quarterly_or_yearly = cash_flow_quarterly_quarter_value
            end_date=cash_flow_quarterly_end_date
        if cash_flow_yearly_date and cash_flow_yearly_year:
            date = cash_flow_yearly_date
            monthly_or_quarterly_or_yearly = cash_flow_yearly_year
            end_date=cash_flow_yearly_end_date
        
        # Create a new CashFlow instance and save form data
        cash_flow_entry = CashFlow(
            company_id = company,
            date = date,  # You can adjust this to take date from form input if required
            end_date=end_date,
            operating_cash_flow = parse_post_value(request.POST.get('Operating_Cash_Flow')),
            net_income_from_continuing_operations =parse_post_value(request.POST.get('Net_Income_from_Continuing_Operations')),
            depreciation_and_amortization =parse_post_value(request.POST.get('Depreciation_and_Amortization')),
            change_in_working_capital =parse_post_value(request.POST.get('Change_in_Working_Capital')),
            changes_in_receivables =parse_post_value(request.POST.get('Changes_in_Receivables')),
            change_in_inventory =parse_post_value(request.POST.get('Change_in_Inventory')),
            change_in_hedging_assets_current =parse_post_value(request.POST.get('Change_in_Hedging_Assets_Current')),
            change_in_other_current_assets =parse_post_value(request.POST.get('Change_in_Other_Current_Assets')),
            change_in_payables_and_accrued_expense =parse_post_value(request.POST.get('Change_in_Payables_And_Accrued_Expense')),
            change_in_pension_and_other_post_retirement_benefit_plans_current =parse_post_value(request.POST.get('Change_in_Pension_and_Other_Post_Retirement_Benefit_Plans_Current')),
            change_in_current_debt_and_capital_lease_obligation =parse_post_value(request.POST.get('Change_in_Current_Debt_And_Capital_Lease_Obligation')),
            change_in_current_deferred_liabilities =parse_post_value(request.POST.get('Change_in_Current_Deferred_Liabilities')),
            change_in_other_current_liabilities =parse_post_value(request.POST.get('Change_in_Other_Current_Liabilities')),
            investing_cash_flow =parse_post_value(request.POST.get('Investing_Cash_Flow')),
            cash_flow_from_continuing_investing_activities =parse_post_value(request.POST.get('Cash_Flow_from_Continuing_Investing_Activities')),
            net_ppe_purchase_and_sale =parse_post_value(request.POST.get('Net_PPE_Purchase_And_Sale')),
            goodwill_and_other_intangible_assets =parse_post_value(request.POST.get('Goodwill_and_Other_Intangible_Assets')),
            investments_and_advances =parse_post_value(request.POST.get('Investments_and_Advances')),
            other_non_current_assets =parse_post_value(request.POST.get('Other_Non_Current_Assets')),
            financing_cash_flow =parse_post_value(request.POST.get('Financing_Cash_Flow')),
            cash_flow_from_continuing_financing_activities =parse_post_value(request.POST.get('Cash_Flow_from_Continuing_Financing_Activities')),
            long_term_debt_and_capital_lease_obligation =parse_post_value(request.POST.get('Long_Term_Debt_and_Capital_Lease_Obligation')),
            non_current_deferred_liabilities =parse_post_value(request.POST.get('Non_Current_Deferred_Liabilities')),
            trade_and_other_payables_non_current =parse_post_value(request.POST.get('Trade_and_Other_Payables_Non_Current')),
            other_non_current_liabilities =parse_post_value(request.POST.get('Other_Non_Current_Liabilities')),
            common_stock_issuance_payments =parse_post_value(request.POST.get('Common_Stock_Issuance_or_Payments')),
            common_stock_dividend_paid =parse_post_value(request.POST.get('Common_Stock_Dividend_Paid')),
            end_cash_position =parse_post_value(request.POST.get('End_Cash_Position')),
            changes_in_cash =parse_post_value(request.POST.get('Changes_in_Cash')),
            beginning_cash_position =parse_post_value(request.POST.get('Beginning_Cash_Position')),
            capital_expenditure =parse_post_value(request.POST.get('Capital_Expenditure')),
            issuance_repurchase_of_capital_stock =parse_post_value(request.POST.get('Issuance_or_Repurchase_of_Capital_Stock')),
            repayment_of_debt =parse_post_value(request.POST.get('Repayment_of_Debt')),
            free_cash_flow =parse_post_value(request.POST.get('Free_Cash_Flow')),
            monthly_or_quarterly_or_yearly = monthly_or_quarterly_or_yearly,  # Add this field to the form
            
        )
        cash_flow_entry.save() 
        income = IncomeStatement.objects.filter(
            company_id=id,
            monthly_or_quarterly_or_yearly=monthly_or_quarterly_or_yearly,
            end_date=end_date
            ).first()

        balance = BalanceSheet.objects.filter(
            company_id=id,
            monthly_or_quarterly_or_yearly=monthly_or_quarterly_or_yearly,
            end_date=end_date
            ).first()
        cash_flow_ratios = CashFlowRatios(
            company_id=company,
            cashflowsheet=cash_flow_entry,
            current_ratio=(safe_decimal1(balance.current_assets) / safe_decimal1(balance.current_liabilities)) if balance.current_liabilities else Decimal(0),
            quick_ratio=((safe_decimal1(balance.current_assets) - safe_decimal1(balance.inventory)) / safe_decimal1(balance.current_liabilities)) if balance.current_liabilities else Decimal(0),
            cash_ratio=(safe_decimal1(balance.cash_and_cash_equivalents) / safe_decimal1(balance.current_liabilities)) if balance.current_liabilities else Decimal(0),
            working_capital=(safe_decimal1(balance.current_assets) - safe_decimal1(balance.current_liabilities)),
            operating_cash_flow_ratio=(safe_decimal1(cash_flow_entry.operating_cash_flow) / safe_decimal1(balance.current_liabilities)) if balance.current_liabilities else Decimal(0),
            debt_service_coverage_ratio=(safe_decimal1(income.operating_income) / safe_decimal1(balance.other_non_current_liabilities)) if balance.other_non_current_liabilities else Decimal(0)
            )
        cash_flow_ratios.save()
        income_ratios = IncomeStatementRatios.objects.filter(
        company_id=id,
        incomesheet=income
        ).first()

        if income_ratios:
            income_ratios.operating_cash_flow_ratio = (safe_decimal1(cash_flow_entry.operating_cash_flow) / safe_decimal1(balance.current_liabilities)) if balance.current_liabilities else Decimal(0)
            income_ratios.debt_service_coverage_ratio =(safe_decimal1(income.operating_income) / safe_decimal1(balance.other_non_current_liabilities)) if balance.other_non_current_liabilities else Decimal(0)
        income_ratios.save()

        balance_ratios = BalanceSheetRatios.objects.filter(
        company_id=id,
        balancesheet=balance
        ).first()

        if balance_ratios:
            balance_ratios.operating_cash_flow_ratio =(safe_decimal1(cash_flow_entry.operating_cash_flow) / safe_decimal1(balance.current_liabilities)) if balance.current_liabilities else Decimal(0)
            balance_ratios.debt_service_coverage_ratio =(safe_decimal1(income.operating_income) / safe_decimal1(balance.other_non_current_liabilities)) if balance.other_non_current_liabilities else Decimal(0)
        balance_ratios.save()
        return redirect('planning_budgeting_cash_flow_table', id)  # Redirect after successful save

    else:
        company = Company.objects.get(company_id=id)
        context = {'company': company}
        return render(request, 'admin/manual_entry_cashflow.html', context)





def cashflowfirstyearofoperations(request, id):
    company = Company.objects.get(company_id=id)
   
    # Retrieve session variables
    cash_flow_monthly_date = request.session.get('cash_flow_monthly_date')
    cash_flow_monthly_end_date = request.session.get('cash_flow_monthly_end_date')
    cash_flow_monthly_month_name = request.session.get('cash_flow_monthly_month_name')
    cash_flow_quarterly_date = request.session.get('cash_flow_quarterly_date')
    cash_flow_quarterly_quarter_value = request.session.get('cash_flow_quarterly_quarter_value')
    cash_flow_yearly_date = request.session.get('cash_flow_yearly_date')
    cash_flow_yearly_year = request.session.get('cash_flow_yearly_year')
    cash_flow_yearly_end_date = request.session.get('cash_flow_yearly_end_date')
    cash_flow_quarterly_end_date = request.session.get('cash_flow_quarterly_end_date')

    # Initialize variables
    date = None
    monthly_or_quarterly_or_yearly = None
    end_date = None
    
    # Determine which period (monthly, quarterly, yearly) we are dealing with
    if cash_flow_monthly_date and cash_flow_monthly_month_name:
        date = cash_flow_monthly_date
        monthly_or_quarterly_or_yearly = 'monthly'
        month_or_quarter_or_year_name = cash_flow_monthly_month_name

        end_date = cash_flow_monthly_end_date
    elif cash_flow_quarterly_date and cash_flow_quarterly_quarter_value:
        date = cash_flow_quarterly_date
        monthly_or_quarterly_or_yearly = 'quaterly'
        month_or_quarter_or_year_name = cash_flow_quarterly_quarter_value

        end_date = cash_flow_quarterly_end_date
    elif cash_flow_yearly_date and cash_flow_yearly_year:
        date = cash_flow_yearly_date
        monthly_or_quarterly_or_yearly = 'yearly'
        month_or_quarter_or_year_name = cash_flow_yearly_year

        end_date = cash_flow_yearly_end_date
    income = IncomeStatement.objects.get(
            company_id=id,
            monthly_or_quarterly_or_yearly=monthly_or_quarterly_or_yearly,
            date=date,
            end_date=end_date
            )
    # print(income)

    balance = BalanceSheet.objects.get(
            company_id=id,
            monthly_or_quarterly_or_yearly=monthly_or_quarterly_or_yearly,
            date=date,
            end_date=end_date
    )
    print(balance.end_date)
    # Check if the previous period data exists
    if date and end_date:
       
        try:
            
            income = IncomeStatement.objects.get(
            company_id=id,
            monthly_or_quarterly_or_yearly=monthly_or_quarterly_or_yearly,
            date=date,
            end_date=end_date
            )
            print(income.end_date)

            balance = BalanceSheet.objects.get(
            company_id=id,
            monthly_or_quarterly_or_yearly=monthly_or_quarterly_or_yearly,
            date=date,
            end_date=end_date
            )
            
            # Perform cash flow calculations
            net_income_from_continuing_operations = income.net_income
            depreciation_and_amortization = income.depreciation_and_amortization
            changes_in_receivables = 0 - balance.receivables
            changes_in_inventory = 0 - balance.inventory
            change_in_hedging_assets_current = 0 - balance.hedging_current_assets
            change_in_payables_and_accrued_expense = balance.payables_and_accrued_expenses
            change_in_other_current_assets = 0 - balance.other_current_assets
            change_in_pension_and_other_post_retirement_benefit_plans_current = balance.pension_and_other_post_retirement_benefit_plans_current
            change_in_current_debt_and_capital_lease_obligation = balance.current_debt_and_capital_lease_obligation
            change_in_current_deferred_liabilities = balance.current_deferred_liabilities
            change_in_other_current_liabilities = balance.other_current_liabilities

            change_in_working_capital = (
                change_in_other_current_liabilities + change_in_current_deferred_liabilities +
                change_in_current_debt_and_capital_lease_obligation +
                change_in_pension_and_other_post_retirement_benefit_plans_current +
                change_in_other_current_assets + change_in_payables_and_accrued_expense +
                change_in_hedging_assets_current + changes_in_inventory + changes_in_receivables
            )

            operating_cash_flow = change_in_working_capital + depreciation_and_amortization + net_income_from_continuing_operations

            net_ppe_purchase_and_sale = 0 - balance.gross_ppe
            goodwill_and_other_intangible_assets = 0 - balance.goodwill_and_other_intangible_assets
            investments_and_advances = 0 - balance.investments_and_advances
            other_non_current_assets = 0 - balance.other_non_current_assets

            cash_flow_from_continuing_investing_activities = (
                net_ppe_purchase_and_sale + goodwill_and_other_intangible_assets +
                investments_and_advances + other_non_current_assets
            )

            investing_cash_flow = cash_flow_from_continuing_investing_activities

            long_term_debt_and_capital_lease_obligation = balance.long_term_debt_and_capital_lease_obligation
            non_current_deferred_liabilities = balance.non_current_deferred_liabilities
            trade_and_other_payables_non_current = balance.trade_and_other_payables_non_current
            other_non_current_liabilities = balance.other_non_current_liabilities
            common_stock_issuance_payments = balance.common_stock+ balance.gains_or_losses_not_affecting_retained_earnings + balance.other_equity_adjustments
            common_stock_dividend_paid = income.equity_share_dividends

            cash_flow_from_continuing_financing_activities = (
                long_term_debt_and_capital_lease_obligation + non_current_deferred_liabilities +
                trade_and_other_payables_non_current + other_non_current_liabilities +
                common_stock_issuance_payments
            ) - common_stock_dividend_paid

            financing_cash_flow = cash_flow_from_continuing_financing_activities
            changes_in_cash = operating_cash_flow + investing_cash_flow + financing_cash_flow
            beginning_cash_position = 0
            capital_expenditure = net_ppe_purchase_and_sale
            issuance_repurchase_of_capital_stock = common_stock_issuance_payments
            repayment_of_debt = long_term_debt_and_capital_lease_obligation
            end_cash_position = changes_in_cash + beginning_cash_position
            free_cash_flow = end_cash_position + capital_expenditure + issuance_repurchase_of_capital_stock + repayment_of_debt

            # Save the calculated cash flow data
            cash_flow_entry = CashFlow(
                company_id=company,
                date=balance.date,
                end_date=balance.end_date,
                operating_cash_flow=operating_cash_flow,
                net_income_from_continuing_operations=net_income_from_continuing_operations,
                depreciation_and_amortization=depreciation_and_amortization,
                change_in_working_capital=change_in_working_capital,
                changes_in_receivables=changes_in_receivables,
                change_in_inventory=changes_in_inventory,
                change_in_hedging_assets_current=change_in_hedging_assets_current,
                change_in_other_current_assets=change_in_other_current_assets,
                change_in_payables_and_accrued_expense=change_in_payables_and_accrued_expense,
                change_in_pension_and_other_post_retirement_benefit_plans_current=change_in_pension_and_other_post_retirement_benefit_plans_current,
                change_in_current_debt_and_capital_lease_obligation=change_in_current_debt_and_capital_lease_obligation,
                change_in_current_deferred_liabilities=change_in_current_deferred_liabilities,
                change_in_other_current_liabilities=change_in_other_current_liabilities,
                investing_cash_flow=investing_cash_flow,
                cash_flow_from_continuing_investing_activities=cash_flow_from_continuing_investing_activities,
                net_ppe_purchase_and_sale=net_ppe_purchase_and_sale,
                goodwill_and_other_intangible_assets=goodwill_and_other_intangible_assets,
                investments_and_advances=investments_and_advances,
                other_non_current_assets=other_non_current_assets,
                financing_cash_flow=financing_cash_flow,
                cash_flow_from_continuing_financing_activities=cash_flow_from_continuing_financing_activities,
                long_term_debt_and_capital_lease_obligation=long_term_debt_and_capital_lease_obligation,
                non_current_deferred_liabilities=non_current_deferred_liabilities,
                trade_and_other_payables_non_current=trade_and_other_payables_non_current,
                other_non_current_liabilities=other_non_current_liabilities,
                common_stock_issuance_payments=common_stock_issuance_payments,
                common_stock_dividend_paid=common_stock_dividend_paid,
                end_cash_position=end_cash_position,
                changes_in_cash=changes_in_cash,
                beginning_cash_position=beginning_cash_position,
                capital_expenditure=capital_expenditure,
                issuance_repurchase_of_capital_stock=issuance_repurchase_of_capital_stock,
                repayment_of_debt=repayment_of_debt,
                free_cash_flow=free_cash_flow,
                monthly_or_quarterly_or_yearly = monthly_or_quarterly_or_yearly,
                month_or_quarter_or_year_name = month_or_quarter_or_year_name
            )
            cash_flow_entry.save()
            cash_flow_ratios = CashFlowRatios(
            company_id=company,
            cashflowsheet=cash_flow_entry,
            current_ratio=(safe_decimal1(balance.current_assets) / safe_decimal1(balance.current_liabilities)) if balance.current_liabilities else Decimal(0),
            quick_ratio=((safe_decimal1(balance.current_assets) - safe_decimal1(balance.inventory)) / safe_decimal1(balance.current_liabilities)) if balance.current_liabilities else Decimal(0),
            cash_ratio=(safe_decimal1(balance.cash_and_cash_equivalents) / safe_decimal1(balance.current_liabilities)) if balance.current_liabilities else Decimal(0),
            working_capital=(safe_decimal1(balance.current_assets) - safe_decimal1(balance.current_liabilities)),
            operating_cash_flow_ratio=(safe_decimal1(cash_flow_entry.operating_cash_flow) / safe_decimal1(balance.current_liabilities)) if balance.current_liabilities else Decimal(0),
            debt_service_coverage_ratio=(safe_decimal1(income.operating_income) / safe_decimal1(balance.other_non_current_liabilities)) if balance.other_non_current_liabilities else Decimal(0)
            )
            cash_flow_ratios.save()
            income_ratios = IncomeStatementRatios.objects.filter(
            company_id=id,
            incomesheet=income
            ).first()

            if income_ratios:
                income_ratios.operating_cash_flow_ratio = (safe_decimal1(cash_flow_entry.operating_cash_flow) / safe_decimal1(balance.current_liabilities)) if balance.current_liabilities else Decimal(0)
                income_ratios.debt_service_coverage_ratio =(safe_decimal1(income.operating_income) / safe_decimal1(balance.other_non_current_liabilities)) if balance.other_non_current_liabilities else Decimal(0)
            income_ratios.save()

            balance_ratios = BalanceSheetRatios.objects.filter(
            company_id=id,
            balancesheet=balance
            ).first()

            if balance_ratios:
                balance_ratios.operating_cash_flow_ratio =(safe_decimal1(cash_flow_entry.operating_cash_flow) / safe_decimal1(balance.current_liabilities)) if balance.current_liabilities else Decimal(0)
                balance_ratios.debt_service_coverage_ratio =(safe_decimal1(income.operating_income) / safe_decimal1(balance.other_non_current_liabilities)) if balance.other_non_current_liabilities else Decimal(0)
            balance_ratios.save()

            return redirect('planning_budgeting_cash_flow_table', id)

        except (IncomeStatement.DoesNotExist, BalanceSheet.DoesNotExist):
            # Insufficient data
            error = "Insufficient data for the selected period."
            context = {'error': error, 'company': company}
            return render(request, 'admin/cash_flow_table.html', context)
    else:
        error = "Insufficient data for the selected period."
        context = {'error': error, 'company': company}
        return render(request, 'admin/cash_flow_table.html', context)


        


def cashFlow(request,id):
    company = Company.objects.get(company_id=id)
    cash_flow = CashFlow.objects.filter(company_id=id).last()
    if request.method == 'POST':
        cash_flow.operating_cash_flow = cash_flow.net_income_from_continuing_operations + cash_flow.depreciation_and_amortization + cash_flow.change_in_working_capital
        
    else:
        context = {'company': company, 'cash_flows': cash_flow}
        return redirect('planning_budgeting_cash_flow_table', id)


    


def get_months_quarters_years():
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    quarters = ["Q1 Jan,Feb,Mar", "Q2 Apr,May,Jun", "Q3 Jul,Aug,Sep", "Q4 Oct,Nov,Dec"]
    years = [str(year) for year in range(2000, 2025)]  
    return months, quarters, years

def get_next_period_headers(start_period, period_type):
    if period_type == 'monthly':
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        start_index = months.index(start_period)
        headers = []
        for i in range(8):
            index = (start_index + i) % 12
            year = 2024 + (start_index + i) // 12  
            headers.append(f"{months[index]} {year}")
        return headers
    elif period_type == 'quarterly':
        quarters = ["Q1 Jan,Feb,Mar", "Q2 Apr,May,Jun", "Q3 Jul,Aug,Sep", "Q4 Oct,Nov,Dec"]
        start_index = quarters.index(start_period)
        headers = []
        for i in range(8):
            index = (start_index + i) % 4
            year = 2024 + (start_index + i) // 4  
            headers.append(f"{quarters[index]} {year}")
        return headers
    elif period_type == 'yearly':
        start_year = int(start_period)
        headers = []
        for i in range(8):
            headers.append(str(start_year + i))
        return headers
    return []




def forecastedIncomeStatementTable1(request, id):
    company = Company.objects.get(company_id=id)
    months, quarters, years = get_months_quarters_years()
    income_statements = IncomeStatement.objects.filter(company_id=id)

    if request.method == 'POST':
        # Handle POST request here
        pass

    else:
        pre_selected_income_statement = request.GET.get('pre_selected_income_statement')
        period_type = 'monthly'  # Default to monthly
        headers = []

        if pre_selected_income_statement:
            if any(pre_selected_income_statement.startswith(month) for month in months):
                period_type = 'monthly'
                headers = get_next_period_headers(pre_selected_income_statement, period_type)
            elif pre_selected_income_statement.startswith('Q'):
                period_type = 'quarterly'
                headers = get_next_period_headers(pre_selected_income_statement, period_type)
            elif pre_selected_income_statement.isdigit():
                period_type = 'yearly'
                headers = get_next_period_headers(pre_selected_income_statement, period_type)

        pre_selected_income_statement_data = IncomeStatement.objects.filter(
            company_id=id,
            month_or_quarter_or_year_name = pre_selected_income_statement
        ).first()

        context = {
            'company': company,
            'months': months,
            'quarters': quarters,
            'years': years,
            'income_statements': income_statements,
            'pre_selected_income_statement_data': pre_selected_income_statement_data,
            'headers': headers,
            'period_type': period_type,
        }

        return render(request, 'admin/forecasted_income_statement.html', context)



def forecastedIncomeStatementTable(request, id):
    company = Company.objects.get(company_id=id)
    months, quarters, years = get_months_quarters_years()
    income_statements = IncomeStatement.objects.filter(company_id=id)
    forecasted_income_statements = ForecastingIncomeStatement.objects.filter(company_id=id)

    if request.method == 'POST':
        # Retrieve the data from the POST request
        income_statement_data = json.loads(request.POST.get('income_statement_data', ''))
        selected_header = request.POST.get('selected_header', '')

        # Print or use the selected header as needed
        

        # Find or create the IncomeStatementData object for the specific company
        income_statement_instance = ForecastingIncomeStatement(company_id=company, month_or_quarter_or_year_name=selected_header)

        # Map the breakdowns to the corresponding model fields
        field_mapping = {
            'Total Revenue': 'total_revenue',
            'Operating Revenue':'operating_revenue',
            'Cost of Revenue':'cost_of_revenue',
            'Gross Profit':'gross_profit',
            'Operating Expenses':'operating_expense',
            'Selling, General and Administrative Expense':'selling_general_and_administrative_expense',
            'General & Administrative Expenses':'general_and_administrative_expenses',
            'Selling and Marketing Expense':'selling_and_marketing_expense',
            'Research and Development Expense':'research_and_development_expense',
            'Operating Income':'operating_income',
            'Net Non Operating Interest Income/ (Expense)':'net_non_operating_interest_income_expense',
            'Interest Income Non Operating':'interest_income_non_operating',
            'Interest Expense Non Operating':'interest_expense_non_operating',
            'Other Income/(Expense)':'other_income_or_expense',
            'Gain/(Loss) on Sale of Security':'gain_or_loss_on_sale_of_security',
            'Special Income/(Charges)':'special_income_or_charges',
            'Write Off':'write_off',
            'Other Non Operating Income/ (Expenses)':'other_non_operating_income_or_expenses',
            'Pretax Income':'pretax_income',
            'Tax Provision':'tax_provision',
            'Net Income':'net_income',
            'Preference Share Dividends':'preference_share_dividends',
            'Net Income to Common Stockholders':'net_income_to_common_stockholders',
            'Equity Share Dividends':'equity_share_dividends',
            'No of Equity Shares':'no_of_equity_shares',
            'Retained Earnings':'retained_earnings',
            'Basic EPS':'abasic_eps',
            'Diluted EPS':'diluted_eps',
            'Depreciation and Amortization':'depreciation_and_amortization',
            'EBITDA':'ebitda',



            
        }

        # Save each breakdown and its corresponding data to the appropriate field
        for item in income_statement_data:
            breakdown = item['breakdown'].strip()
            values_data = {}
            growth_rates_data = {}

            # Assuming the periods are fixed and known
            periods = ['preselected', 'period1', 'period2', 'period3', 'period4', 'period5', 'period6', 'period7']

            # Assign values and growth rates to respective periods
            for i, period in enumerate(periods):
                values_data[period] = item['data'][i * 2]  # Get value for the period
                growth_rates_data[period] = item['data'][i * 2 + 1]  # Get growth rate for the period

            # Prepare the final structure
            data = {
                'periods': values_data,
                'growth_rates': growth_rates_data
            }

            # Set the data to the corresponding field
            field_name = field_mapping.get(breakdown)
            if field_name:
                setattr(income_statement_instance, field_name, data)

        # Save the instance
        income_statement_instance.save()

        return redirect('forecasting_income_statement_table', id)

    else:
        pre_selected_income_statement = request.GET.get('pre_selected_income_statement')
        forecasted_income_statement = request.GET.get('forecasted_income_statement')
        #print(forecasted_income_statement,'forecasted_income_statement')

        period_type = 'monthly'  # Default to monthly
        headers = []

        if pre_selected_income_statement:
            if any(pre_selected_income_statement.startswith(month) for month in months):
                period_type = 'monthly'
                headers = get_next_period_headers(pre_selected_income_statement, period_type)
            elif pre_selected_income_statement.startswith('Q'):
                period_type = 'quarterly'
                headers = get_next_period_headers(pre_selected_income_statement, period_type)
            elif pre_selected_income_statement.isdigit():
                period_type = 'yearly'
                headers = get_next_period_headers(pre_selected_income_statement, period_type)

        if forecasted_income_statement:
            if any(forecasted_income_statement[0:8].startswith(month) for month in months):
                period_type = 'monthly'
                headers = get_next_period_headers(forecasted_income_statement[0:8], period_type)
            elif forecasted_income_statement.startswith('Q'):
                period_type = 'quarterly'
                headers = get_next_period_headers(forecasted_income_statement, period_type)
            elif forecasted_income_statement.isdigit():
                period_type = 'yearly'
                headers = get_next_period_headers(forecasted_income_statement, period_type)

        pre_selected_income_statement_data = IncomeStatement.objects.filter(
            company_id=id,
            month_or_quarter_or_year_name=pre_selected_income_statement
        ).first()

        forecasted_income_statement_data = ForecastingIncomeStatement.objects.filter(
            company_id=id,
            month_or_quarter_or_year_name=forecasted_income_statement
        ).first()

        context = {
            'company': company,
            'months': months,
            'quarters': quarters,
            'years': years,
            'income_statements': income_statements,
            'forecasted_income_statements': forecasted_income_statements,
            'pre_selected_income_statement_data': pre_selected_income_statement_data,
            'forecasted_income_statement_data': forecasted_income_statement_data,
            'headers': headers,
            'period_type': period_type,
        }

        return render(request, 'admin/forecasted_income_statement.html', context)


def forecastedBalanceSheetTable1(request, id):
    company = Company.objects.get(company_id=id)
    months, quarters, years = get_months_quarters_years()
    balance_sheets = BalanceSheet.objects.filter(company_id=id)

    if request.method == 'POST':
        # Handle POST request here
        pass

    else:
        pre_selected_balance_sheet = request.GET.get('pre_selected_balance_sheet')
        period_type = 'monthly'  # Default to monthly
        headers = []

        if pre_selected_balance_sheet:
            if any(pre_selected_balance_sheet.startswith(month) for month in months):
                period_type = 'monthly'
                headers = get_next_period_headers(pre_selected_balance_sheet, period_type)
            elif pre_selected_balance_sheet.startswith('Q'):
                period_type = 'quarterly'
                headers = get_next_period_headers(pre_selected_balance_sheet, period_type)
            elif pre_selected_balance_sheet.isdigit():
                period_type = 'yearly'
                headers = get_next_period_headers(pre_selected_balance_sheet, period_type)

        pre_selected_balance_sheet_data = BalanceSheet.objects.filter(
            company_id=id,
            month_or_quarter_or_year_name=pre_selected_balance_sheet
        ).first()

        context = {
            'company': company,
            'months': months,
            'quarters': quarters,
            'years': years,
            'balance_sheets': balance_sheets,
            'pre_selected_balance_sheet_data': pre_selected_balance_sheet_data,
            'headers': headers,
            'period_type': period_type,
        }

        return render(request, 'admin/forecasted_balance_sheet.html', context)



def forecastedBalanceSheetTable(request, id):
    company = Company.objects.get(company_id=id)
    months, quarters, years = get_months_quarters_years()
    balance_sheets = BalanceSheet.objects.filter(company_id=id)
    forecasted_balance_sheets = ForecastingBalanceSheet.objects.filter(company_id=id)

    if request.method == 'POST':
        # Retrieve the data from the POST request
        balance_sheet_data = json.loads(request.POST.get('balance_sheet_data', ''))
        selected_header = request.POST.get('selected_header', '')

        # Print or use the selected header as needed
       

        # Find or create the BalanceSheetData object for the specific company
        balance_sheet_instance = ForecastingBalanceSheet(company_id=company, month_or_quarter_or_year_name=selected_header)

        # Map the breakdowns to the corresponding model fields
        field_mapping = {
            'Total Assets': 'total_assets',
            'Current Assets': 'current_assets',
            'Cash, Cash Equivalents & Short Term Investments':'cash_cash_equivalents_and_short_term_investments',
            'Cash And Cash Equivalents': 'cash_and_cash_equivalents',
            'Cash':'cash',
            'Cash Equivalents':'cash_equivalents',
            'Other Short Term Investments':'other_short_term_investments',
            'Receivables': 'receivables',
            'Accounts receivable':'accounts_receivable',
            'Gross Accounts Receivable':'gross_accounts_receivable',
            'Allowance For Doubtful Accounts Receivable':'allowance_for_doubtful_accounts_receivable',
            'Other receivables':'other_receivables',
            'Inventory': 'inventory',
            'Raw Materials':'raw_materials',
            'Work in Process':'work_in_process',
            'Finished Goods':'finished_goods',
            'Hedging Current Assets':'hedging_current_assets',
            'Other Current Assets':'other_current_assets',
            'Total non-current assets':'total_non_current_assets',
            'Net PPE':'net_ppe',
            'Gross PPE':'gross_ppe',
            'Land And Improvements':'land_and_improvements',
            'Buildings And Improvements':'buildings_and_improvements',
            'Machinery Furniture Equipment':'machinery_furniture_equipment',
            'Other Properties':'other_properties',
            'Leases':'leases',
            'Accumulated Depreciation':'accumulated_depreciation',
            'Goodwill And Other Intangible Assets':'goodwill_and_other_intangible_assets',
            'Goodwill':'goodwill',
            'Other Intangible Assets': 'other_intangible_assets',
            'Investments And Advances':'investments_and_advances',
            'Long Term Equity Investment':'long_term_equity_investment',
            'Other Non Current Assets':'other_non_current_assets',
            'Total Liabilities Net Minority Interest':'total_liabilities_net_minority_interest',
            'Current Liabilities':'current_liabilities',
            'Payables And Accrued Expenses':'payables_and_accrued_expenses',
            'Accounts Payable':'accounts_payable',
            'Income Tax Payable':'income_tax_payable',
            'Pension & Other Post Retirement Benefit Plans Current':'pension_and_other_post_retirement_benefit_plans_current',
            'Current Debt And Capital Lease Obligation':'current_debt_and_capital_lease_obligation',
            'Current Debt':'current_debt',
            'Capital Lease Obligation':'capital_lease_obligation',
            'Current Deferred Liabilities':'current_deferred_liabilities',
            'Current Deferred Revenue':'current_deferred_revenue',
            'Other Current Liabilities':'other_current_liabilities',
            'Total Non Current Liabilities Net Minority Interest':'total_non_current_liabilities_net_minority_interest',
            'Long Term Debt And Capital Lease Obligation':'long_term_debt_and_capital_lease_obligation',
            'Long Term Debt':'long_term_debt',
            'Long Term Capital Lease Obligation':'long_term_capital_lease_obligation',
            'Non Current Deferred Liabilities':'non_current_deferred_liabilities',
            'Non Current Deferred Taxes Liabilities':'non_current_deferred_taxes_liabilities',
            'Non Current Deferred Revenue':'non_current_deferred_revenue',
            'Trade and Other Payables Non Current':'trade_and_other_payables_non_current',
            'Other Non Current Liabilities':'other_non_current_liabilities',
            'Total Equity Gross Minority Interest':'total_equity_gross_minority_interest',
            'Stockholders Equity':'stockholders_equity',
            'Capital Stock':'capital_stock',
            'Common Stock':'common_stock',
            'Retained Earnings':'retained_earnings',
            'Gains/ (Losses) Not Affecting Retained Earnings':'gains_or_losses_not_affecting_retained_earnings',
            'Other Equity Adjustments':'other_equity_adjustments',



            
        }

        # Save each breakdown and its corresponding data to the appropriate field
        for item in balance_sheet_data:
            breakdown = item['breakdown'].strip()
            values_data = {}
            growth_rates_data = {}

            # Assuming the periods are fixed and known
            periods = ['preselected', 'period1', 'period2', 'period3', 'period4', 'period5', 'period6', 'period7']

            # Assign values and growth rates to respective periods
            for i, period in enumerate(periods):
                values_data[period] = item['data'][i * 2]  # Get value for the period
                growth_rates_data[period] = item['data'][i * 2 + 1]  # Get growth rate for the period

            # Prepare the final structure
            data = {
                'periods': values_data,
                'growth_rates': growth_rates_data
            }

            # Set the data to the corresponding field
            field_name = field_mapping.get(breakdown)
            if field_name:
                setattr(balance_sheet_instance, field_name, data)

        # Save the instance
        balance_sheet_instance.save()

        return redirect('forecasting_balance_sheet_table', id)

    else:
        pre_selected_balance_sheet = request.GET.get('pre_selected_balance_sheet')
        forecasted_balance_sheet = request.GET.get('forecasted_balance_sheet')

        period_type = 'monthly'  # Default to monthly
        headers = []

        if pre_selected_balance_sheet:
            if any(pre_selected_balance_sheet.startswith(month) for month in months):
                period_type = 'monthly'
                headers = get_next_period_headers(pre_selected_balance_sheet, period_type)
            elif pre_selected_balance_sheet.startswith('Q'):
                period_type = 'quarterly'
                headers = get_next_period_headers(pre_selected_balance_sheet, period_type)
            elif pre_selected_balance_sheet.isdigit():
                period_type = 'yearly'
                headers = get_next_period_headers(pre_selected_balance_sheet, period_type)

        if forecasted_balance_sheet:
            if any(forecasted_balance_sheet[0:8].startswith(month) for month in months):
                period_type = 'monthly'
                headers = get_next_period_headers(forecasted_balance_sheet[0:8], period_type)
            elif forecasted_balance_sheet.startswith('Q'):
                period_type = 'quarterly'
                headers = get_next_period_headers(forecasted_balance_sheet, period_type)
            elif forecasted_balance_sheet.isdigit():
                period_type = 'yearly'
                headers = get_next_period_headers(forecasted_balance_sheet, period_type)

        pre_selected_balance_sheet_data = BalanceSheet.objects.filter(
            company_id=id,
            month_or_quarter_or_year_name=pre_selected_balance_sheet
        ).first()

        forecasted_balance_sheet_data = ForecastingBalanceSheet.objects.filter(
            company_id=id,
            month_or_quarter_or_year_name=forecasted_balance_sheet
        ).first()

        context = {
            'company': company,
            'months': months,
            'quarters': quarters,
            'years': years,
            'balance_sheets': balance_sheets,
            'forecasted_balance_sheets': forecasted_balance_sheets,
            'pre_selected_balance_sheet_data': pre_selected_balance_sheet_data,
            'forecasted_balance_sheet_data': forecasted_balance_sheet_data,
            'headers': headers,
            'period_type': period_type,
        }

        return render(request, 'admin/forecasted_balance_sheet.html', context)

def forecastedCashFlowTable1(request, id):
    company = Company.objects.get(company_id=id)
    months, quarters, years = get_months_quarters_years()
    cash_flows = CashFlow.objects.filter(company_id=id)
    forecasted_cash_flows = ForecastingCashFlow.objects.filter(company_id=id)
    


    
    if request.method == 'POST':
        # Retrieve the data from POST request
        cash_flow_data = json.loads(request.POST.get('cash_flow_data', ''))
        selected_header = request.POST.get('selected_header', '')
         # Print or use the selected header as needed
   
        # Find or create the CashFlowData object for the specific company
        #company_id = request.POST.get('company_id')  # Ensure company_id is sent in the POST request
        #cash_flow_instance, created = CashFlowData.objects.get_or_create(company_id=company_id)
        cash_flow_instance = ForecastingCashFlow(company_id=company,month_or_quarter_or_year_name=selected_header)

        # Map the breakdowns to the corresponding model fields
        field_mapping = {
            'Operating Cash Flow': 'operating_cash_flow',
            'Net Income from Continuing Operations': 'net_income_from_continuing_operations',
            'Depreciation & amortization': 'depreciation_and_amortization',
            'Change in working capital': 'change_in_working_capital',
            'Changes in Receivables': 'changes_in_receivables',
            'Change in Inventory': 'change_in_inventory',
            'Change in Hedging Assets Current': 'change_in_hedging_assets_current',
            'Change in Other Current Assets': 'change_in_other_current_assets',
            'Change in Payables And Accrued Expense': 'change_in_payables_and_accrued_expense',
            'Change in Pension & Other Post Retirement Benefit Plans Current': 'change_in_pension_and_other_post_retirement_benefit_plans_current',
            'Change in Current Debt And Capital Lease Obligation': 'change_in_current_debt_and_capital_lease_obligation',
            'Change in Current Deferred Liabilities': 'change_in_current_deferred_liabilities',
            'Change in Other Current Liabilities': 'change_in_other_current_liabilities',
            'Investing Cash Flow': 'investing_cash_flow',
            'Cash Flow from Continuing Investing Activities': 'cash_flow_from_continuing_investing_activities',
            'Net PPE Purchase And Sale': 'net_ppe_purchase_and_sale',
            'Goodwill And Other Intangible Assets': 'goodwill_and_other_intangible_assets',
            'Investments And Advances': 'investments_and_advances',
            'Other Non Current Assets': 'other_non_current_assets',
            'Financing Cash Flow': 'financing_cash_flow',
            'Cash Flow from Continuing Financing Activities': 'cash_flow_from_continuing_financing_activities',
            'Long Term Debt And Capital Lease Obligation': 'long_term_debt_and_capital_lease_obligation',
            'Non Current Deferred Liabilities': 'non_current_deferred_liabilities',
            'Trade and Other Payables Non Current': 'trade_and_other_payables_non_current',
            'Other Non Current Liabilities': 'other_non_current_liabilities',
            'Common Stock Issuance/ (Payments)': 'common_stock_issuance_payments',
            'Common Stock Dividend Paid': 'common_stock_dividend_paid',
            'End Cash Position': 'end_cash_position',
            'Changes in Cash': 'changes_in_cash',
            'Beginning Cash Position': 'beginning_cash_position',
            'Capital Expenditure': 'capital_expenditure',
            'Issuance/ (Repurchase) of Capital Stock': 'issuance_repurchase_of_capital_stock',
            'Repayment of Debt': 'repayment_of_debt',
            'Free Cash Flow': 'free_cash_flow',
        }

        # Save each breakdown and its corresponding data to the appropriate field
        for item in cash_flow_data:
            breakdown = item['breakdown'].strip()
            values_data = {}
            growth_rates_data = {}

            # Assuming the periods are fixed and known
            periods = ['preselected', 'period1', 'period2', 'period3', 'period4', 'period5', 'period6', 'period7']

            # Assign values and growth rates to respective periods
            for i, period in enumerate(periods):
                values_data[period] = item['data'][i*2]  # Get value for the period
                growth_rates_data[period] = item['data'][i*2 + 1]  # Get growth rate for the period

            # Prepare the final structure
            data = {
                'periods': values_data,
                'growth_rates': growth_rates_data
            }

            # Set the data to the corresponding field
            field_name = field_mapping.get(breakdown)
            if field_name:
                setattr(cash_flow_instance, field_name, data)

        # Save the instance
        cash_flow_instance.save()
        

        return redirect('forecasting_cash_flow_table',id)
        pass

    else:
        pre_selected_cash_flow = request.GET.get('pre_selected_cash_flow')
        forecasted_cash_flow = request.GET.get('forecasted_cash_flow')

        period_type = 'monthly'  # Default to monthly
        headers = []

        if pre_selected_cash_flow:
            if any(pre_selected_cash_flow.startswith(month) for month in months):
                period_type = 'monthly'
                headers = get_next_period_headers(pre_selected_cash_flow, period_type)
            elif pre_selected_cash_flow.startswith('Q'):
                period_type = 'quarterly'
                headers = get_next_period_headers(pre_selected_cash_flow, period_type)
            elif pre_selected_cash_flow.isdigit():
                period_type = 'yearly'
                headers = get_next_period_headers(pre_selected_cash_flow, period_type)
        if forecasted_cash_flow:
            #print(forecasted_cash_flow[0:8],forecasted_cash_flow,type(forecasted_cash_flow))

            if any(forecasted_cash_flow[0:8].startswith(month) for month in months):
                period_type = 'monthly'
                headers = get_next_period_headers(forecasted_cash_flow[0:8], period_type)
            elif forecasted_cash_flow.startswith('Q'):
                period_type = 'quarterly'
                headers = get_next_period_headers(forecasted_cash_flow, period_type)
            elif forecasted_cash_flow.isdigit():
                period_type = 'yearly'
                headers = get_next_period_headers(forecasted_cash_flow, period_type)

        pre_selected_cash_flow_data = CashFlow.objects.filter(
            company_id=id,
            month_or_quarter_or_year_name=pre_selected_cash_flow
        ).first()

        forecasted_cash_flow_data = ForecastingCashFlow.objects.filter(
            company_id=id,
            month_or_quarter_or_year_name = forecasted_cash_flow
        ).first()
        context = {
            'company': company,
            'months': months,
            'quarters': quarters,
            'years': years,
            'cash_flows': cash_flows,
            'forecasted_cash_flows':forecasted_cash_flows,
            'pre_selected_cash_flow_data': pre_selected_cash_flow_data,
            'forecasted_cash_flow_data':forecasted_cash_flow_data,
            'headers': headers,
            'period_type': period_type,
        }

        return render(request, 'admin/forecasted_cash_flow.html', context)


def forecastedCashFlowTable(request, id):
    company = Company.objects.get(company_id=id)
    months, quarters, years = get_months_quarters_years()
    cash_flows = CashFlow.objects.filter(company_id=id)
    forecasted_cash_flows = ForecastingCashFlow.objects.filter(company_id=id)
    
    if request.method == 'POST':
        # Retrieve the data from POST request
        cash_flow_data = json.loads(request.POST.get('cash_flow_data', ''))
        selected_header = request.POST.get('selected_header', '')
         # Print or use the selected header as needed
       

        # Find or create the CashFlowData object for the specific company
        #company_id = request.POST.get('company_id')  # Ensure company_id is sent in the POST request
        #cash_flow_instance, created = CashFlowData.objects.get_or_create(company_id=company_id)
        cash_flow_instance = ForecastingCashFlow(company_id=company,month_or_quarter_or_year_name=selected_header)

        # Map the breakdowns to the corresponding model fields
        field_mapping = {
            'Operating Cash Flow': 'operating_cash_flow',
            'Net Income from Continuing Operations': 'net_income_from_continuing_operations',
            'Depreciation & amortization': 'depreciation_and_amortization',
            'Change in working capital': 'change_in_working_capital',
            'Changes in Receivables': 'changes_in_receivables',
            'Change in Inventory': 'change_in_inventory',
            'Change in Hedging Assets Current': 'change_in_hedging_assets_current',
            'Change in Other Current Assets': 'change_in_other_current_assets',
            'Change in Payables And Accrued Expense': 'change_in_payables_and_accrued_expense',
            'Change in Pension & Other Post Retirement Benefit Plans Current': 'change_in_pension_and_other_post_retirement_benefit_plans_current',
            'Change in Current Debt And Capital Lease Obligation': 'change_in_current_debt_and_capital_lease_obligation',
            'Change in Current Deferred Liabilities': 'change_in_current_deferred_liabilities',
            'Change in Other Current Liabilities': 'change_in_other_current_liabilities',
            'Investing Cash Flow': 'investing_cash_flow',
            'Cash Flow from Continuing Investing Activities': 'cash_flow_from_continuing_investing_activities',
            'Net PPE Purchase And Sale': 'net_ppe_purchase_and_sale',
            'Goodwill And Other Intangible Assets': 'goodwill_and_other_intangible_assets',
            'Investments And Advances': 'investments_and_advances',
            'Other Non Current Assets': 'other_non_current_assets',
            'Financing Cash Flow': 'financing_cash_flow',
            'Cash Flow from Continuing Financing Activities': 'cash_flow_from_continuing_financing_activities',
            'Long Term Debt And Capital Lease Obligation': 'long_term_debt_and_capital_lease_obligation',
            'Non Current Deferred Liabilities': 'non_current_deferred_liabilities',
            'Trade and Other Payables Non Current': 'trade_and_other_payables_non_current',
            'Other Non Current Liabilities': 'other_non_current_liabilities',
            'Common Stock Issuance/ (Payments)': 'common_stock_issuance_payments',
            'Common Stock Dividend Paid': 'common_stock_dividend_paid',
            'End Cash Position': 'end_cash_position',
            'Changes in Cash': 'changes_in_cash',
            'Beginning Cash Position': 'beginning_cash_position',
            'Capital Expenditure': 'capital_expenditure',
            'Issuance/ (Repurchase) of Capital Stock': 'issuance_repurchase_of_capital_stock',
            'Repayment of Debt': 'repayment_of_debt',
            'Free Cash Flow': 'free_cash_flow',
        }

        # Save each breakdown and its corresponding data to the appropriate field
        for item in cash_flow_data:
            breakdown = item['breakdown'].strip()
            values_data = {}
            growth_rates_data = {}

            # Assuming the periods are fixed and known
            periods = ['preselected', 'period1', 'period2', 'period3', 'period4', 'period5', 'period6', 'period7']

            # Assign values and growth rates to respective periods
            for i, period in enumerate(periods):
                values_data[period] = item['data'][i*2]  # Get value for the period
                growth_rates_data[period] = item['data'][i*2 + 1]  # Get growth rate for the period

            # Prepare the final structure
            data = {
                'periods': values_data,
                'growth_rates': growth_rates_data
            }

            # Set the data to the corresponding field
            field_name = field_mapping.get(breakdown)
            if field_name:
                setattr(cash_flow_instance, field_name, data)

        # Save the instance
        cash_flow_instance.save()
        

        return redirect('forecasting_cash_flow_table',id)
        pass

    else:
        pre_selected_cash_flow = request.GET.get('pre_selected_cash_flow')
        forecasted_cash_flow = request.GET.get('forecasted_cash_flow')

        period_type = 'monthly'  # Default to monthly
        headers = []

        if pre_selected_cash_flow:
            if any(pre_selected_cash_flow.startswith(month) for month in months):
                period_type = 'monthly'
                headers = get_next_period_headers(pre_selected_cash_flow, period_type)
            elif pre_selected_cash_flow.startswith('Q'):
                period_type = 'quarterly'
                headers = get_next_period_headers(pre_selected_cash_flow, period_type)
            elif pre_selected_cash_flow.isdigit():
                period_type = 'yearly'
                headers = get_next_period_headers(pre_selected_cash_flow, period_type)
        if forecasted_cash_flow:
            #print(forecasted_cash_flow[0:8],forecasted_cash_flow,type(forecasted_cash_flow))

            if any(forecasted_cash_flow[0:8].startswith(month) for month in months):
                period_type = 'monthly'
                headers = get_next_period_headers(forecasted_cash_flow[0:8], period_type)
            elif forecasted_cash_flow.startswith('Q'):
                period_type = 'quarterly'
                headers = get_next_period_headers(forecasted_cash_flow, period_type)
            elif forecasted_cash_flow.isdigit():
                period_type = 'yearly'
                headers = get_next_period_headers(forecasted_cash_flow, period_type)

        pre_selected_cash_flow_data = CashFlow.objects.filter(
            company_id=id,
            month_or_quarter_or_year_name=pre_selected_cash_flow
        ).first()

        forecasted_cash_flow_data = ForecastingCashFlow.objects.filter(
            company_id=id,
            month_or_quarter_or_year_name = forecasted_cash_flow
        ).first()

        context = {
            'company': company,
            'months': months,
            'quarters': quarters,
            'years': years,
            'cash_flows': cash_flows,
            'forecasted_cash_flows':forecasted_cash_flows,
            'pre_selected_cash_flow_data': pre_selected_cash_flow_data,
            'forecasted_cash_flow_data':forecasted_cash_flow_data,
            'headers': headers,
            'period_type': period_type,
        }

        return render(request, 'admin/forecasted_cash_flow.html', context)   

#Investor

def investorDashboard(request):
    users = User.objects.filter(company_type='investor')
    companies = []
    for user in users:
        companies.extend(user.companies.all())
    
    sector=Sector.objects.all()    
    # for company in companies:
    #     print(company.company_type)
    return render(request, 'investor/dashboard.html', {'companies': companies, 'industries':sector})

def investorBase(request,id):
    company=Company.objects.get(company_id=id)
    user=User.objects.get(user_id=company.user_id)
    context={
        'company':company,
        'user':user
    }
    return render(request, 'investor/base.html', context)


def basicInformation(request, id):
    company = get_object_or_404(Company, company_id=id)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            company.name = data.get('company-name', company.name)
            company.email = data.get('email', company.email)
            company.phone = data.get('phone', company.phone) 
            company.date_of_incorporation = data.get('founded-in', company.date_of_incorporation) 
            company.website_url = data.get('website', company.website_url)
            company.linkedin_url = data.get('linkedin', company.linkedin_url)
            company.location = data.get('address', company.location)
            company.no_of_employees = data.get('number-of-employees', company.no_of_employees)
            company.business_type = data.get('business-type', company.business_type)
            company.vision = data.get('company-vision', company.vision)
            company.products = data.get('products-services', company.products)
            company.competitor = data.get('key-competitors', company.competitor)
            company.customers = data.get('number-of-customers', company.customers)
            company.additional = data.get('additional-info', company.additional)
            company.current_revenue = data.get('revenue_current_year', company.current_revenue)
            company.current_pl = data.get('profit_current_year', company.current_pl)
            company.previous_revenue = data.get('revenue_previous_year', company.previous_revenue)
            company.previous_pl = data.get('profit_previous_year', company.previous_pl)
            company.a_yearbefore_revenue = data.get('revenue_year_before', company.a_yearbefore_revenue)
            company.a_yearbefore_pl = data.get('profit_year_before', company.a_yearbefore_pl)

            company.save()

            return JsonResponse({'message': 'Details saved successfully!'})
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON data')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    context = {'company': company}
    return render(request, 'investor/basic_information.html', context)



def founderAndTeam(request,id):
    company = Company.objects.get(company_id = id)
    user=User.objects.get(user_id=company.user_id)

    founders = Founder.objects.filter(company_id = id)
    context = { 'company':company,
        'user':user,'founders':founders}
    return render(request,'investor/founders_and_team.html',context)
#New one
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from .models import Company, Founder

def founders(request, id):
    if request.method == 'POST':
        name = request.POST.get('name')
        title = request.POST.get('title')
        linkedin_url = request.POST.get('linkedin_url')
        short_profile = request.POST.get('short_profile')
        photo = request.FILES.get('photo')
        founder_id=request.POST.get('id')
        date=request.POST.get('date_joined')
        company = get_object_or_404(Company, company_id=id)

        try:
            if founder_id:
                # Update existing founder
                founder = Founder.objects.get(id=founder_id)
                founder.name = name
                founder.title = title
                founder.linkedin_url = linkedin_url
                founder.short_profile = short_profile
                founder.date_joined=date
                if photo:
                    founder.photo = photo
                founder.save()
                return JsonResponse({'success': True})
            else:
                # Create new founder
                Founder.objects.create(
                    name=name,
                    title=title,
                    linkedin_url=linkedin_url,
                    short_profile=short_profile,
                    photo=photo,
                    company_id=company,
                    date_joined=date
                )
                return JsonResponse({'success': True})
        except Founder.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Founder not found'})

    else:
        founders = Founder.objects.filter(company_id=id)
        company = Company.objects.get(company_id=id)
        
        context = {
            'founder': founders,
            'company': company
        }
        return render(request, 'admin/founders.html', context)





    

#Editor
def editorDashboard(request):
    return render(request,'editor/dashboard.html')

def parent(request):
    subuser_context = custom_subuser(request)
    current_subuser = subuser_context.get('current_subuser') 
    creator_id = current_subuser.creator_id
    creator_data=User.objects.get(user_id = creator_id)
    context ={'creator_data':creator_data}
    return render(request,'editor/parent.html',context)

#User
def userDashboard(request):
    return render(request,'user/dashboard.html')

#Password Reset 
import random
def generate_random_otp():
    otp = ""
    for i in range(5):
        otp += str(random.randint(0, 9))
    return otp
#generate_random_otp()
#print("Generated OTP:", generate_otp())

def forgotPasswordOne(request):
    if request.method == 'POST':
        input_email = request.POST['email']
       
        if User.objects.filter(email=input_email).exists() or Team.objects.filter(email=input_email).exists():
            generated_otp = generate_random_otp()
            request.session['OTP'] = generated_otp
            request.session['email'] = input_email
            # Debug print statements
            # print("OTP set in session:", request.session.get('OTP'))
            # print("Email set in session:", request.session.get('email'))
            # Get the current site domain
            current_site = get_current_site(request)
            domain = current_site.domain

            # Construct the signin URL
            password_reset_url = f'http://{domain}/forgot_password_2'

            subject='Number Leader - Password Reset Link'
            txt='''
                Password Reset Link and OTP :

                OTP: {}
                Domain: {}

                    '''
            message=txt.format(generated_otp,password_reset_url)
            from_email=settings.EMAIL_HOST_USER
            to_list=[input_email]
            send_mail(subject, message,from_email,to_list,fail_silently=True)
            messages.success(request,'we have sent opt to your mail please check')
            return redirect('forgot_password_1')
        else:
            messages.error(request,'please enter the registered email')
            return redirect('forgot_password_1')
    else:
        return render(request,'forgot_password_1.html')


def forgotPasswordTwo(request):
    if request.method == 'POST':
        input_otp = int(request.POST['otp'])
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        session_otp = request.session.get('OTP')
        session_email =request.session.get('email')
        

        if 'OTP' in request.session and 'email' in request.session:
            if input_otp == int(session_otp):
                if User.objects.filter(email=session_email).exists():
                    if new_password == confirm_new_password:
                        user = User.objects.get(email=session_email)
                        user.password = confirm_new_password
                        user.save()
                        del request.session['OTP'] 
                        del request.session['email']
                        messages.error(request,'Password reset completed sucessfully')
                        return redirect('forgot_password_2')

                if Team.objects.filter(email=session_email):
                    if new_password == confirm_new_password:
                        team = Team.objects.get(email=session_email)
                        team.password = confirm_new_password
                        team.save()
                        
                        del request.session['OTP'] 
                        del request.session['email']
                        messages.error(request,'Password reset completed sucessfully')
                        return redirect('forgot_password_2')
                    else:
                        messages.error(request,'Both Password Must be same')
                        return redirect('forgot_password_2')   
                else:
                    messages.error(request,'Please generate OTP first')
                    return redirect('forgot_password_2')
            else:
                messages.error(request,'Please enter correct otp')
                return redirect('forgot_password_2')
        else:
            messages.error(request,'Please generate OTP first')
            return redirect('forgot_password_2')
        
    else:
        return render(request,'forgot_password_2.html')



def company_ask(request, id):
    if request.method == 'POST':

        try:
            data = json.loads(request.body)
            ask = data.get('ask')
            value = data.get('value')
            equityShare = data.get('equityShare')
            details = data.get('details')
            
            # Fetch the company based on ID
            company = Company.objects.get(company_id=id)
            
            # Assuming you have a model named Ask to store this data
            company_ask_instance = Ask(
                ask=ask,
                valuation=value,
                equity_share=equityShare,
                details=details,
                company=company  # Link the data to the company
            )

            # Save the instance to the database
            company_ask_instance.save()
            
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:    
        company=Company.objects.get(company_id=id)
        ask=Ask.objects.filter(company=id)
        context={'company': company,
                 'ask': ask}
        return render(request, 'admin/company_ask.html', context)


def get_end_date_balance_sheet_and_income_statement(end_date, company):
    balance_sheet = BalanceSheet.objects.filter(company_id=company, end_date=end_date).first()
    income_statement = IncomeStatement.objects.filter(company_id=company, end_date=end_date).first()
    return balance_sheet, income_statement







@csrf_exempt
def save_edited_data(request, company_id):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            edited_data = data.get('editedData', [])
            if not edited_data:
                return JsonResponse({'error': 'No edited data provided'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        # Define a mapping between front-end field names and model field names
        field_name_mapping = {
            'cash': 'cash',
            'cash-equivalents': 'cash_equivalents',
            'other-short-term-investments': 'other_short_term_investments',
            'gross-accounts-receivable': 'gross_accounts_receivable',
            'allowance-for-doubtful-accounts-receivable': 'allowance_for_doubtful_accounts_receivable',
            'other-receivables': 'other_receivables',
            'land_and_improvements': 'land_and_improvements',
            'buildings_and_improvements': 'buildings_and_improvements',
            'machinery_furniture_equipment': 'machinery_furniture_equipment',
            'other_properties': 'other_properties',
            'accumulated_depreciation': 'accumulated_depreciation',
            'goodwill': 'goodwill',
            'other_intangible_assets': 'other_intangible_assets',
            'long_term_equity_investment': 'long_term_equity_investment',
            'other_non_current_assets': 'other_non_current_assets',
            'accounts-payable': 'accounts_payable',
            'income-tax-payable': 'income_tax_payable',
            'current-debt': 'current_debt',
            'capital-lease': 'capital_lease_obligation',
            'current-deferred-revenue': 'current_deferred_revenue',
            'other-current-liabilities': 'other_current_liabilities',
            'long-term-debt': 'long_term_debt',
            'long-term-capital-lease-obligation': 'long_term_capital_lease_obligation',
            'non-current-deferred-taxes-liabilities': 'non_current_deferred_taxes_liabilities',
            'non-current-deferred-revenue': 'non_current_deferred_revenue',
            'trade-and-other-payables-non-current': 'trade_and_other_payables_non_current',
            'other-non-current-liabilities': 'other_non_current_liabilities',
            'capital-stock': 'capital_stock',
            'common-stock': 'common_stock',
            'retained-earnings': 'retained_earnings',
            'gains_losses_not_affecting_retained_earnings': 'gains_or_losses_not_affecting_retained_earnings',
            'other-equity-adjustments': 'other_equity_adjustments',
            'total_assets': 'total_assets',
            'current-assets': 'current_assets',
            'cash-cash-equivalents-and-short-term': 'cash_cash_equivalents_and_short_term_investments',
            'cash-and-cash-equivalents': 'cash_and_cash_equivalents',
            'receivables': 'receivables',
            'accounts-receivable': 'accounts_receivable',
            'inventory': 'inventory',
            'raw-materials': 'raw_materials',
            'work-process': 'work_in_process',
            'finished-goods': 'finished_goods',
            'hedging-assets': 'hedging_current_assets',
            'other-current-assets': 'other_current_assets',
            'total_non_current_assets': 'total_non_current_assets',
            'net_ppe': 'net_ppe',
            'gross_ppe': 'gross_ppe',
            'leases': 'leases',
            'goodwill_and_other_intangible_assets': 'goodwill_and_other_intangible_assets',
            'investments_and_advances': 'investments_and_advances',
            'total-liabilities-net-minority-interest': 'total_liabilities_net_minority_interest',
            'current-liabilities': 'current_liabilities',
            'payables-and-accrued-expenses': 'payables_and_accrued_expenses',
            'accounts-payable': 'accounts_payable',
            'income-tax-payable': 'income_tax_payable',
            'pension-post-retirement': 'pension_and_other_post_retirement_benefit_plans_current',
            'current-debt-and-capital-lease-obligation': 'current_debt_and_capital_lease_obligation',
            'current-debt': 'current_debt',
            'capital-lease': 'capital_lease',
            'current-deferred-liabilities': 'current_deferred_liabilities',
            'current-deferred-revenue': 'current_deferred_revenue',
            'other-current-liabilities': 'other_current_liabilities',
            'total-non-current-liabilities-net-minority-interest': 'total_non_current_liabilities_net_minority_interest',
            'long-term-debt-and-capital-lease-obligation': 'long_term_debt_and_capital_lease_obligation',
            'long-term-debt': 'long_term_debt',
            'long-term-capital-lease-obligation': 'long_term_capital_lease_obligation',
            'non-current-deferred-liabilities': 'non_current_deferred_liabilities',
            'non-current-deferred-taxes-liabilities': 'non_current_deferred_taxes_liabilities',
            'non-current-deferred-revenue': 'non_current_deferred_revenue',
            'trade-and-other-payables-non-current': 'trade_and_other_payables_non_current',
            'other-non-current-liabilities': 'other_non_current_liabilities',
            'total-equity-gross-minority-interest': 'total_equity_gross_minority_interest',
            'stockholders-equity': 'stockholders_equity',
        }
        errors=[]
        balance_sheets_to_update = set()

        for column in edited_data:
            values = column.get('values', [])
            if not values:
                continue  # Skip if no values in the column

            # Extract endDate and periodType
            end_date = column.get('values')[-1].get('endDate')
            period_type = column.get('values')[-1].get('periodType')

            if not end_date or not period_type:
                return JsonResponse({'error': 'endDate or periodType missing in one of the columns'}, status=400)

            try:
                balance_sheet = BalanceSheet.objects.get(
                    company_id=company_id,
                    end_date=end_date,
                    monthly_or_quarterly_or_yearly=period_type
                )
            except BalanceSheet.DoesNotExist:
                return JsonResponse({
                    'error': f'BalanceSheet record not found for end_date: {end_date}, period_type: {period_type}'
                }, status=404)

            for value_data in values[:-1]:  # Skipping last items (endDate, periodType)
                front_end_field_name = value_data.get('fieldName')
                value = value_data.get('value')

                if not front_end_field_name:
                    continue  # Skip if fieldName is missing

                model_field_name = field_name_mapping.get(front_end_field_name)

                if model_field_name:
                    try:
                        if value == '' or value is None:
                            value = 0  # Assign default value if it's empty

                        # Convert to number
                        if isinstance(value, str) and '.' in value:
                            value = round(float(value))
                        else:
                            value = int(value)

                        setattr(balance_sheet, model_field_name, value)

                    except ValueError:
                        return JsonResponse({'error': f"Field '{model_field_name}' expected a number but got '{value}'."}, status=400)

            # Save balance sheet changes
            balance_sheet.save()
            # Add balance sheet to the set for ratio/cash flow update
            balance_sheets_to_update.add(balance_sheet)

        # Now update ratios and cash flow after all columns are processed
        for balance_sheet in balance_sheets_to_update:
            try:
                # Update balance sheet ratios
                ratios, created = BalanceSheetRatios.objects.get_or_create(
                    company_id=company_id,
                    balancesheet=balance_sheet
                )
                ratios.current_ratio = (balance_sheet.current_assets / balance_sheet.current_liabilities) if balance_sheet.current_liabilities else 0
                ratios.quick_ratio = ((balance_sheet.current_assets - balance_sheet.inventory) / balance_sheet.current_liabilities) if balance_sheet.current_liabilities else 0
                ratios.cash_ratio = (balance_sheet.cash_and_cash_equivalents / balance_sheet.current_liabilities) if balance_sheet.current_liabilities else 0
                ratios.working_capital = (balance_sheet.current_assets - balance_sheet.current_liabilities)
                ratios.debt_equity_ratio = (balance_sheet.other_non_current_liabilities / balance_sheet.stockholders_equity) if balance_sheet.stockholders_equity else 0
                ratios.debt_ratio = (balance_sheet.other_non_current_liabilities / balance_sheet.total_assets) if balance_sheet.total_assets else 0
                ratios.equity_ratio = (balance_sheet.stockholders_equity / balance_sheet.total_assets) if balance_sheet.total_assets else 0
                ratios.debt_capital_ratio = (balance_sheet.other_non_current_liabilities / (balance_sheet.stockholders_equity + balance_sheet.other_non_current_liabilities)) if (balance_sheet.stockholders_equity + balance_sheet.other_non_current_liabilities) else 0
                ratios.save()

                # Update cash flow
                period_exists, previous_period_date, previous_balance_sheet, previous_income_statement = check_previous_entry_exists(
                    balance_sheet.end_date, company_id, balance_sheet.monthly_or_quarterly_or_yearly
                )
                current_income_statement = get_end_date_balance_sheet_and_income_statement(
                    balance_sheet.end_date, company_id
                )[1]
                
                if not period_exists or not current_income_statement:
                    return JsonResponse({'error': f'Previous or current period data not found for end_date: {balance_sheet.end_date}, period_type: {balance_sheet.monthly_or_quarterly_or_yearly}.'}, status=404)

                # Calculate current cash flow
                cash_flow_data = calculate_cash_flow(
                    balance_sheet, current_income_statement, previous_balance_sheet, previous_income_statement
                )
                CashFlow.objects.update_or_create(
                    company_id=company_id,
                    end_date=balance_sheet.end_date,
                    defaults=cash_flow_data
                )

                # Check next period data
                next_period_exists, next_period_date, next_balance_sheet, next_income_statement = get_next_period_data(
                    balance_sheet.end_date, company_id, balance_sheet.monthly_or_quarterly_or_yearly
                )
                print(next_balance_sheet, next_income_statement, balance_sheet, current_income_statement)
                if next_period_exists and next_balance_sheet and next_income_statement:
                    cash_flow_data1 = calculate_cash_flow(
                        next_balance_sheet, next_income_statement, balance_sheet, current_income_statement
                    )
                    CashFlow.objects.update_or_create(
                        company_id=company_id,
                        end_date=next_balance_sheet.end_date,
                        defaults=cash_flow_data1
                    )
                else:
                    errors.append(f'Next period balance sheet or income statement not found for column.')

            except Exception as e:
                return JsonResponse({'error': f"Error updating for end_date {balance_sheet.end_date}: {str(e)}"}, status=500)

        return JsonResponse({'message': 'All BalanceSheets, Cash Flows, and Ratios updated successfully!'})

    return JsonResponse({'error': 'Invalid request method'}, status=405)




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import IncomeStatement, CashFlow, Company



from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
@csrf_exempt
def save_edited_data_income(request, company_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            edited_data = data.get('editedData', [])
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        field_name_mapping = {
            'total_revenue': 'total_revenue',
            'operating_revenue': 'operating_revenue',
            'cost_of_revenue': 'cost_of_revenue',
            'gross_profit': 'gross_profit',
            'operating_expense': 'operating_expense',
            'selling_general_and_administrative_expense': 'selling_general_and_administrative_expense',
            'general_and_administrative_expenses': 'general_and_administrative_expenses',
            'selling_and_marketing_expense': 'selling_and_marketing_expense',
            'research_and_development_expense': 'research_and_development_expense',
            'operating_income': 'operating_income',
            'net_non_operating_interest_income_expense': 'net_non_operating_interest_income_expense',
            'interest_income_non_operating': 'interest_income_non_operating',
            'interest_expense_non_operating': 'interest_expense_non_operating',
            'other_income_or_expense': 'other_income_or_expense',
            'gain_or_loss_on_sale_of_security': 'gain_or_loss_on_sale_of_security',
            'special_income': 'special_income',
            'write_off': 'write_off',
            'other_non_operating_income_or_expenses': 'other_non_operating_income_or_expenses',
            'pretax_income': 'pretax_income',
            'tax_provision': 'tax_provision',
            'net_income': 'net_income',
            'preference_share_dividends': 'preference_share_dividends',
            'net_income_to_common_stockholders': 'net_income_to_common_stockholders',
            'equity_share_dividends': 'equity_share_dividends',
            'retained_earnings': 'retained_earnings',
            'basic_eps': 'basic_eps',
            'diluted_eps': 'diluted_eps',
            'depreciation_and_amortization': 'depreciation_and_amortization',
            'no_of_equity_shares': 'no_of_equity_shares',
            'ebitda': 'ebitda',
        }

        errors = []
        for column in edited_data:
            column_index = column.get('columnIndex')
            values = column.get('values', [])

            if not values:
                errors.append(f"Skipping empty columnIndex {column_index}")
                continue

            try:
                end_date_str = values[-1].get('endDate')
                period_type = values[-1].get('periodType')
                end_date = datetime.strptime(end_date_str, '%d-%m-%Y').date()

                income_statement, created = IncomeStatement.objects.get_or_create(
                    company_id=company_id,
                    end_date=end_date,
                    monthly_or_quarterly_or_yearly=period_type
                )

                for value_data in values[:-2]:
                    front_end_field_name = value_data.get('fieldName')
                    value = value_data.get('value')

                    model_field_name = field_name_mapping.get(front_end_field_name)

                    if model_field_name and value is not None:
                        if value == '' or value is None:
                            value = 0
                        if '.' in str(value):
                            value = round(float(value))
                        else:
                            value = int(value)

                        setattr(income_statement, model_field_name, value)

                income_statement.save()

                # Calculate and save ratios
                ratios, _ = IncomeStatementRatios.objects.get_or_create(
                    company_id=company_id,
                    incomesheet=income_statement
                )

                ratios.gross_profit_ratio = (income_statement.gross_profit / income_statement.operating_revenue) if income_statement.operating_revenue else 0
                ratios.operating_profit_ratio = (income_statement.operating_income / income_statement.operating_revenue) if income_statement.operating_revenue else 0
                ratios.ebitda_margin = (income_statement.ebitda / income_statement.total_revenue) if income_statement.total_revenue else 0
                ratios.net_profit_margin = (income_statement.net_income / income_statement.total_revenue) if income_statement.total_revenue else 0
                ratios.earnings_per_share = (income_statement.net_income_to_common_stockholders / income_statement.no_of_equity_shares) if income_statement.no_of_equity_shares else 0
                ratios.interest_service = (income_statement.operating_income / income_statement.interest_expense_non_operating) if income_statement.interest_expense_non_operating else 0

                ratios.save()

                # Fetch previous period data
                period_exists, previous_period_date, previous_balance_sheet, previous_income_statement = check_previous_entry_exists(end_date, company_id, period_type)
                balance_sheet = get_end_date_balance_sheet_and_income_statement(end_date, company_id)[0]

                if not period_exists or not balance_sheet:
                    errors.append(f'Previous balance sheet or income statement not found for the provided date for column {column_index}.')
                    continue

                cash_flow_data = calculate_cash_flow(balance_sheet, income_statement, previous_balance_sheet, previous_income_statement)

                cash_flow, _ = CashFlow.objects.get_or_create(company_id=company_id, end_date=end_date, monthly_or_quarterly_or_yearly=income_statement.monthly_or_quarterly_or_yearly)
                for key, value in cash_flow_data.items():
                    setattr(cash_flow, key, value)
                cash_flow.save()

                # Fetch next period data
                next_period_exists, next_period_date, next_balance_sheet, next_income_statement = get_next_period_data(end_date, company_id, period_type)

                # Check if next period data exists
                if not next_period_exists or not next_balance_sheet:
                    errors.append(f'Next period balance sheet or income statement not found for column {column_index}.')
                    continue

                # Calculate cash flow for next period
                cash_flow_data1 = calculate_cash_flow(next_balance_sheet, next_income_statement, balance_sheet, income_statement)

                # Save next period cash flow data
                cash_flow1, _ = CashFlow.objects.get_or_create(company_id=company_id, end_date=next_balance_sheet.end_date)
                for key, value in cash_flow_data1.items():
                    setattr(cash_flow1, key, value)
                cash_flow1.save()

            except Exception as e:
                errors.append(f"Error processing columnIndex {column_index}: {str(e)}")

        if errors:
            return JsonResponse({'errors': errors}, status=400)

        return JsonResponse({'message': 'IncomeStatement, Cash Flow, and Ratios updated successfully for all columns!'})

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt  # If you are handling CSRF in headers, this can be removed
def delete_cap_table_entry(request, id):
    if request.method == 'DELETE':
        print(id)
        try:
            # Fetch the object using entry_id
            entry = CapTable.objects.get(id=id)
            entry.delete()  # Delete the entry
            return JsonResponse({'message': 'Entry deleted successfully.'}, status=200)
        except CapTable.DoesNotExist:
            return JsonResponse({'error': 'Entry not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import CapTable
import json
from datetime import datetime

@csrf_exempt
@require_http_methods(["PUT"])
def update_cap_table_entry(request, id):
    try:
        # Parse JSON body
        data = json.loads(request.body)
        print(data)

        # Fetch the CapTableEntry object by id
        try:
            entry = CapTable.objects.get(id=id)
        except CapTable.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Entry not found'}, status=404)

        # Validate and update fields
        if 'shareholder' in data:
            entry.shareholder = data['shareholder'] or None  # Allow empty values to be None

        if 'name' in data:
            entry.name = data['name']

        if 'equityShare' in data:
            try:
                entry.percentage_of_shares = float(data['equityShare'])  # Convert string to decimal if needed
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid equityShare value'}, status=400)

        if 'investedSince' in data:
            try:
                if data['investedSince']:
                    entry.investedsince = datetime.strptime(data['investedSince'], '%Y-%m-%d').date()
                else:
                    entry.investedsince = None  # Handle empty strings
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid date format for investedSince'}, status=400)

        if 'investmentAmount' in data:
            entry.amount = data.get('investmentAmount') or None

        if 'valuation' in data:
            entry.valuation = data.get('valuation') or None

        if 'details' in data:
            entry.details = data['details'] or None

        # Save the updated entry
        entry.save()

        return JsonResponse({'success': True})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        print(f"Error updating CapTable entry: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt  # If you are handling CSRF in headers, this can be removed
def delete_ask_entry(request, id):
    if request.method == 'DELETE':
        print(id)
        try:
            # Fetch the object using entry_id
            entry = Ask.objects.get(id=id)
            entry.delete()  # Delete the entry
            return JsonResponse({'message': 'Entry deleted successfully.'}, status=200)
        except Ask.DoesNotExist:
            return JsonResponse({'error': 'Entry not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
 # Assuming CompanyAsk is your model for the company ask data

@require_http_methods(["DELETE"])
def delete_company_ask(request, company_id, entry_id):
    try:
        entry = get_object_or_404(Ask,  id=entry_id)
        entry.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404

import json

@require_http_methods(["PUT"])
def update_entry(request, company_id, entry_id):
    try:
        entry = get_object_or_404(Ask, company=company_id, id=entry_id)
        data = json.loads(request.body)

        # Update the entry with the new data
        entry.ask = data.get('ask')
        entry.valuation = data.get('valuation')
        entry.equity_share = data.get('equityShare')
        entry.details = data.get('details')
        entry.save()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_http_methods(["GET"])
def get_entry(request, entry_id):
    try:
        entry = get_object_or_404(Ask, id=entry_id)
        # Return the current values of the entry
        data = {
            'ask': entry.ask,
            'valuation': entry.valuation,
            'equityShare': entry.equity_share,
            'details': entry.details,
        }
        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Founder

@require_http_methods(["DELETE"])
def delete_founder(request, founder_id):
    try:
        founder = get_object_or_404(Founder, id=founder_id)
        founder.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def news(request, id):
    company = get_object_or_404(Company, company_id=id)
    news = news.objects.filter(company_id=id)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            news_date = data.get('date')
            summary = data.get('summary')
            link = data.get('link')
            
            # Convert the date string to a date object
            if news_date:
                news_date = datetime.strptime(news_date, '%Y-%m-%d').date()

            new_entry = news.objects.create(
                company_id=company,
                date=news_date,
                news_summary=summary,
                website_link=link
            )
            new_entry.save()
            return JsonResponse({'status': 'success', 'data': data})
        except Exception as e:
            #traceback.print_exc()
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    context = {'company': company, 'news': news}
    return render(request, 'admin/news.html', context)




from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def capTable(request, id):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)

            
            name = data.get('name')
            shareholder = data.get('shareholder')
            percentage_of_shares = data.get('equityShare')
            investedsince = data.get('investedSince')
            amount = data.get('investmentAmount')
            valuation = data.get('valuation')
            details = data.get('details')

            # Fetch the associated company object
            company = Company.objects.get(company_id=id)

            # Create a new CapTable entry
            CapTable.objects.create(
                company_id=company,
                name=name,
                shareholder=shareholder,
                percentage_of_shares=percentage_of_shares,
                investedsince=investedsince,
                amount=amount,
                valuation=valuation,
                details=details
            )

            # Return a success response
            return JsonResponse({'success': True, 'message': 'Entry saved successfully'})

        except json.JSONDecodeError:
            # Handle JSON decode error
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        except Company.DoesNotExist:
            # Handle case where company does not exist
            return JsonResponse({'error': 'Company not found'}, status=404)

    elif request.method == 'GET':
        company = Company.objects.get(company_id=id)
     
        cap_table = CapTable.objects.filter(company_id=id)

        context = {
            'company': company,
           
            'cap_table': cap_table
        }

        return render(request, 'admin/cap_table.html', context)
    


@require_http_methods(["GET"])
def get_entry(request, entry_id):
    try:
        entry = get_object_or_404(Ask, id=entry_id)
        # Return the current values of the entry
        data = {
            'ask': entry.ask,
            'valuation': entry.valuation,
            'equityShare': entry.equity_share,
            'details': entry.details,
        }
        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Founder



# def businessPlan(request, id):
    
#     company = Company.objects.get(company_id = id)


#     try:
#         plan_files = plan_finacials.objects.filter(company_id = id)              
#         last_rec = plan_files.aggregate(Max('line_no'))['line_no__max']              
#     except:
#         plan_files = None        
#         last_rec = None        

#     try:
#         products = productsandservices.objects.all()
#     except:
#         products = None

#     context = {
#         'company':company,
      
#         'plan_files':plan_files,        
#         'last_rec':last_rec,
#         'products':products       
#     }

#     if request.method == 'POST':
        
#         b_files = request.FILES.get('b_files')
#         f_files = request.FILES.get('f_files')
#         line_no = request.POST.get('line_no')
#         p_name = request.POST.get('p_name')
                

#         try:
#             ext_file =  plan_finacials.objects.get(company_id = id, line_no = line_no)     
#         except:
#             ext_file = None
        
#         if ext_file:
#             if b_files:
#                 if ext_file.b_plan_pdf:                    
#                     if default_storage.exists(ext_file.b_plan_pdf.path):
#                         default_storage.delete(ext_file.b_plan_pdf.path)                
#                 ext_file.b_plan_pdf = b_files
#                 ext_file.p_name = p_name
#                 ext_file.save()

#             if f_files:
#                 if ext_file.f_plan_pdf:                    
#                     if default_storage.exists(ext_file.f_plan_pdf.path):
#                         default_storage.delete(ext_file.f_plan_pdf.path)                
#                 ext_file.f_plan_pdf = f_files
#                 ext_file.p_name = p_name
#                 ext_file.save()   

#             return JsonResponse({'message': 'Details updated successfully!'})      
            
#         else:                              
#             plan_finacials_new = plan_finacials(
#                 company_id = company, 
#                 line_no = line_no,           
#                 b_plan_pdf = b_files,
#                 f_plan_pdf = f_files,
#                 p_name = p_name
#             )
#             plan_finacials_new.save()

#             return JsonResponse({'message': 'Details saved successfully!'})  

#     else:
#         return render(request, 'admin/businessdocs.html', context)        
    
def remove_file(request):    
    line_no = request.GET.get('line_no')
    file_type = request.GET.get('type')  # 'b' for b_plan_pdf, 'f' for f_plan_pdf
    
    if line_no is None or file_type not in ['b', 'f']:
        return JsonResponse({'error': 'Invalid request parameters.'}, status=400)
    
    # Get the plan_finacials record based on the line_no
    try:
        plan_file = get_object_or_404(plan_finacials, line_no=line_no)
    except plan_finacials.DoesNotExist:
        return JsonResponse({'error': 'File not found.'}, status=404)

    # Determine the file to delete
    if file_type == 'b':
        file_path = plan_file.b_plan_pdf.path
        plan_file.b_plan_pdf.delete(save=False)
    elif file_type == 'f':
        file_path = plan_file.f_plan_pdf.path
        plan_file.f_plan_pdf.delete(save=False)

    # Delete the file from the file system
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Check if both files are now empty and delete the record if so
    if not plan_file.b_plan_pdf and not plan_file.f_plan_pdf:
        plan_file.delete()
    else:
        plan_file.save()

    return JsonResponse({'message': 'File removed successfully.'})


def news_post(request, id):
    company = Company.objects.get(company_id=id)

    current_date = datetime.now().date()

    try:
        news_data = Company_news.objects.filter(company_id=id)
        last_rec = news_data.aggregate(Max('line_no'))['line_no__max']
    except:
        news_data = None
        last_rec = None

    context = {
        'company': company,
        'current_date': current_date,
        'news_data': news_data,
        'last_rec': last_rec
    }

    if request.method == 'POST':
        line_no = request.POST.get('line_no')
        summary = request.POST.get('summary')
        link = request.POST.get('link')

        try:
            old_data = Company_news.objects.get(company_id=id, line_no = line_no)
        except:
            old_data = None        

        

        if old_data:            
            old_data.sub_date = current_date
            old_data.summary = summary
            old_data.link = link
            old_data.save()             
            return JsonResponse({'message': 'Details updated successfully!'})     
        else:
            news_new = Company_news(
                 company_id=company, 
                sub_date = current_date,
                line_no=line_no,
                summary=summary,
                link=link
            )
            news_new.save()
            return JsonResponse({'message': 'Details saved successfully!'})        

    return render(request, 'admin/news_post.html', context)


def pitchvideoandppt(request, id):

    company = Company.objects.get(company_id = id)
    

    try:
        ppt_v = companypptandvideo.objects.filter(company_id = id)              
        last_rec = ppt_v.aggregate(Max('line_no'))['line_no__max']              
    except:
        ppt_v = None        
        last_rec = None        

    try:
        products = productsandservices.objects.all()
    except:
        products = None

    context = {
        'company':company,
        
        'ppt_v':ppt_v,        
        'last_rec':last_rec,
        'products':products       
    }


    if request.method == 'POST':
        
        ppt_file = request.FILES.get('ppt_file')
        video_file = request.FILES.get('video_file')
        line_no = request.POST.get('line_no')
        p_name = request.POST.get('p_name')
                

        try:
            ext_file =  companypptandvideo.objects.get(company_id = id, line_no = line_no)     
        except:
            ext_file = None
        
        if ext_file:
            if ppt_file:
                if ext_file.ppt_file:                    
                    if default_storage.exists(ext_file.ppt_file.path):
                        default_storage.delete(ext_file.ppt_file.path)                
                ext_file.ppt_file = ppt_file
                ext_file.p_name = p_name
                ext_file.save()

            if video_file:
                if ext_file.video_file:                    
                    if default_storage.exists(ext_file.video_file.path):
                        default_storage.delete(ext_file.video_file.path)                
                ext_file.video_file = video_file
                ext_file.p_name = p_name
                ext_file.save()     

            return JsonResponse({'message': 'Details updated successfully!'})    
            
        else:                              
            companypptandvideo_new = companypptandvideo(
                company_id = company, 
                line_no = line_no,           
                ppt_file = ppt_file,
                video_file = video_file,
                p_name = p_name
            )
            companypptandvideo_new.save()

            return JsonResponse({'message': 'Details saved successfully!'})  

    else:
        return render(request, 'admin/pitchpptandvideo.html', context)   
import os
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def pitchvideoandppt_remove(request):    
    line_no = request.GET.get('line_no')
    file_type = request.GET.get('type')  # 'b' for PDF, 'ppt' for PPT, 'f' for video
    
    if line_no is None or file_type not in ['b', 'ppt', 'f']:
        return JsonResponse({'error': 'Invalid request parameters.'}, status=400)
    
    try:
        ppt_video = get_object_or_404(companypptandvideo, line_no=line_no)
    except companypptandvideo.DoesNotExist:
        return JsonResponse({'error': 'File not found.'}, status=404)

    # Determine the file to delete based on file_type
    if file_type == 'b':  # PDF (stored in ppt_file)
        file_path = ppt_video.ppt_file.path
        ppt_video.ppt_file.delete(save=False)
    elif file_type == 'ppt':  # PPT (also stored in ppt_file)
        file_path = ppt_video.ppt_file.path
        ppt_video.ppt_file.delete(save=False)
    elif file_type == 'f':  # Video (stored in video_file)
        file_path = ppt_video.video_file.path
        ppt_video.video_file.delete(save=False)
    else:
        return JsonResponse({'error': 'Invalid file type.'}, status=400)

    # Delete the file from the file system
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            return JsonResponse({'error': str(e), 'file_path': file_path}, status=500)
    
    # Check if all files are empty, delete the record if so
    if not ppt_video.ppt_file and not ppt_video.video_file:
        ppt_video.delete()
    else:
        ppt_video.save()

    return JsonResponse({'message': 'File removed successfully.'})



def bench4_files(request, id):
    company = Company.objects.get(company_id=id)

    if request.method == 'POST':
        valuation_doc = request.FILES.get('valuation_doc')
        bench_mark_doc = request.FILES.get('bench_mark_doc')
        line_no = request.POST.get('line_no')

        try:
            ext_file = BenchMark.objects.get(company_id=id, line_no=line_no)
        except BenchMark.DoesNotExist:
            ext_file = None

        if ext_file:
            if valuation_doc:
                if ext_file.valuation_doc and default_storage.exists(ext_file.valuation_doc.path):
                    default_storage.delete(ext_file.valuation_doc.path)
                ext_file.valuation_doc = valuation_doc

            if bench_mark_doc:
                if ext_file.bench_mark_doc and default_storage.exists(ext_file.bench_mark_doc.path):
                    default_storage.delete(ext_file.bench_mark_doc.path)
                ext_file.bench_mark_doc = bench_mark_doc

            ext_file.save()

            return JsonResponse({'message': 'File uploaded successfully!'})

        else:
            new_benchmark = BenchMark(
                company_id=company,
                line_no=line_no,
                valuation_doc=valuation_doc,
                bench_mark_doc=bench_mark_doc
            )
            new_benchmark.save()

            return JsonResponse({'message': 'File uploaded successfully!'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def bench4(request, id):

    print('abcd')

    company = Company.objects.get(company_id = id)
    # company_profile = CompanyProfile.objects.get(company_id = id)

    try:
        bench_dt = BenchMark.objects.filter(company_id = id)              
        last_rec = bench_dt.aggregate(Max('line_no'))['line_no__max']              
    except:
        bench_dt = None        
        last_rec = None        

    try:
        products = productsandservices.objects.all()
    except:
        products = None
    
    com_line = False
    if bench_dt:
        for i in bench_dt:
            if i.line_no == 1:
                com_line = True

    context = {
        'company':company,
        # 'company_profile': company_profile,
        'bench_dt':bench_dt,        
        'last_rec':last_rec,
        'products':products,
        'com_line':com_line       
    }

    if request.method == 'POST':

        print('099989')
        
        line_no = request.POST.get('line_no')
        valuation = request.POST.get('valuation')
        source = request.POST.get('source')
        valuation_dt = request.POST.get('valuation_dt')              
        p_name = request.POST.get('p_name')
     
        try:
            ext_file =  BenchMark.objects.get(company_id = id, line_no = line_no)     
        except:
            ext_file = None

        if ext_file:
            ext_file.valuation = valuation
            ext_file.source = source
            ext_file.valuation_dt = valuation_dt            
            ext_file.p_name = p_name
            ext_file.save()   

            success_msg = 'Details updated successfully!'

            return render(request, 'admin/bench4.html', {'success_msg':success_msg, 'company':company,
                                                           
                                                            'bench_dt':bench_dt,        
                                                            'last_rec':last_rec,
                                                            'products':products,
                                                            'com_line':com_line })   

            # return JsonResponse({'message': 'Details updated successfully!'})       
        else:                
            bench4_new = BenchMark(
                company_id = company, 
                line_no = line_no,           
                valuation = valuation,
                source = source,
                valuation_dt = valuation_dt,                
                p_name = p_name,
            )
            bench4_new.save()

            success_msg = 'Details saved successfully!'
            return render(request, 'admin/bench4.html', {'success_msg':success_msg, 'company':company,
                                                           
                                                            'bench_dt':bench_dt,        
                                                            'last_rec':last_rec,
                                                            'products':products,
                                                            'com_line':com_line }) 
        
            # return JsonResponse({'message': 'Details saved successfully!'})  

    return render(request, 'admin/bench4.html', context)   

  
def remove_bench4_file(request):    
    line_no = request.GET.get('line_no')
    file_type = request.GET.get('type')  # 'b' for benchmark, 'v' for valuation
    
    if line_no is None or file_type not in ['b', 'v']:
        return JsonResponse({'error': 'Invalid request parameters.'}, status=400)
    
    # Get the plan_finacials record based on the line_no
    try:
        bench_file = get_object_or_404(BenchMark, line_no=line_no)
    except plan_finacials.DoesNotExist:
        return JsonResponse({'error': 'File not found.'}, status=404)

    # Determine the file to delete
    if file_type == 'b':
        file_path = bench_file.bench_mark_doc.path
        bench_file.bench_mark_doc.delete(save=False)
    elif file_type == 'v':
        file_path = bench_file.valuation_doc.path
        bench_file.valuation_doc.delete(save=False)

    # Delete the file from the file system
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Check if both files are now empty and delete the record if so
    if not bench_file.bench_mark_doc and not bench_file.valuation_doc:
        bench_file.delete()
    else:
        bench_file.save()

    return JsonResponse({'message': 'File removed successfully.'})


def delete_bench(request, line_no):

    id = request.GET.get('id')

    company = Company.objects.get(company_id = id)
    # company_profile = CompanyProfile.objects.get(company_id = id)
    
    try:
        ext_file =  BenchMark.objects.get(company_id = id, line_no = line_no)     
    except:
        ext_file = None

    
    if ext_file:

        if ext_file.bench_mark_doc:
            file_path = ext_file.bench_mark_doc.path            
            
            if os.path.exists(file_path):
                os.remove(file_path)

        if ext_file.valuation_doc:
            file_path = ext_file.valuation_doc.path
            
            if os.path.exists(file_path):
                os.remove(file_path)


        ext_file.delete()
        success_msg = 'Record deleted successfully!'
        return render(request, 'admin/bench4.html', {'success_msg':success_msg, 'company':company, })
    
    success_msg = 'Something went wrong, Please try again!'
    return render(request, 'admin/bench4.html', {'success_msg':success_msg, 'company':company,})


def addCompany(request):
    if request.method == 'POST':
        user_context = custom_user(request)
        current_user = user_context.get('current_user') 
        name = request.POST.get('name')
        date_of_incorporation = request.POST.get('date_of_incorporation')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        website_url = request.POST.get('website_url')
        linkedin_url = request.POST.get('linkedin_url')
        business_type = request.POST.get('business_type')
        sector = request.POST.get('sector')
        company_type = request.POST.get('company_type')
        location = request.POST.get('location')
        no_of_employees = request.POST.get('no_of_employees')
        products = request.POST.get('products')
        competitor = request.POST.get('competitor')
        vision = request.POST.get('vision')
        customers = request.POST.get('customers')
        current_revenue = request.POST.get('current_revenue')
        current_pl = request.POST.get('current_pl')
        previous_revenue = request.POST.get('previous_revenue')
        previous_pl = request.POST.get('previous_pl')
        a_yearbefore_revenue = request.POST.get('a_yearbefore_revenue')
        a_yearbefore_pl = request.POST.get('a_yearbefore_pl')
        additional = request.POST.get('additional')

        # Create and save the Company instance
        company = Company(
            user_id=current_user,  # Assuming the user is logged in and user_id is provided
            name=name,
            date_of_incorporation=date_of_incorporation,
            email=email,
            phone=phone,
            website_url=website_url,
            linkedin_url=linkedin_url,
            business_type=business_type,
            sector=sector,

            location=location,
            no_of_employees=no_of_employees,
            products=products,
            competitor=competitor,
            vision=vision,
            customers=customers,
            current_revenue=current_revenue,
            current_pl=current_pl,
            previous_revenue=previous_revenue,
            previous_pl=previous_pl,
            a_yearbefore_revenue=a_yearbefore_revenue,
            a_yearbefore_pl=a_yearbefore_pl,
            additional=additional,
            company_type=current_user.company_type
        )
        company.save()
        latest_company = Company.objects.filter(user_id=current_user).latest('company_id')
        id=latest_company.company_id
       
        return redirect('basic_information', id)  # Redirect to a success page
    else:
        sectors = Sector.objects.all()
        business_types = BusinessType.objects.all()
        business_stages = BusinessStage.objects.all()
        context = { 'sectors':sectors,'business_types':business_types,'business_stages':business_stages}
        return render(request,'admin/add_company.html',context)
    

def delete_news(request, news_id):
    # Check if the request method is POST
    print(id)
    if request.method == "POST":
        news_item = get_object_or_404(Company_news, id=news_id)
        news_item.delete()  # Delete the news item

        return JsonResponse({"message": "News item deleted successfully."})
    
    return JsonResponse({"error": "Invalid request method."}, status=400)


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Company_news

def update_news(request, line_no):
    if request.method == "POST":
        news_item = get_object_or_404(Company_news, line_no=line_no)

        # Update the fields with the data sent from the front-end
        news_item.sub_date = request.POST.get('newsDate')  # You can format the date if necessary
        news_item.summary = request.POST.get('summary')
        news_item.link = request.POST.get('link')
        news_item.save()  # Save the updated news item

        return JsonResponse({"message": "News item updated successfully."})

    return JsonResponse({"error": "Invalid request method."}, status=400)
