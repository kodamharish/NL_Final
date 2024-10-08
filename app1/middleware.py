# from django.shortcuts import redirect
# from django.urls import reverse
# from django.utils.deprecation import MiddlewareMixin

# class SessionExpiryMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         login_url = reverse('login')  # Get the URL for the login page
#         if not request.session.get('current_user_id') and not request.session.get('current_subuser_id'):
#             # User is not authenticated if neither session variable is set
#             if request.path != login_url and request.path != reverse('sign_up') and not request.path.startswith('/admin/'):
#                 # Exclude login, signup, and admin paths if needed
#                 return redirect(login_url)  # Redirect to the login page


# from django.shortcuts import redirect
# from django.urls import reverse
# from django.utils.deprecation import MiddlewareMixin

# class SessionExpiryMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         login_url = reverse('login')  # Get the URL for the login page
#         signup_url = reverse('signup')  # Get the URL for the signup page
#         home_url = reverse('home')  # Get the URL for the home page
#         about_url = reverse('about')  # Get the URL for the about page
#         #root_url = reverse('home')  # Assuming '' path maps to home

#         # Define a list of paths to exclude from session check
#         excluded_paths = [login_url, signup_url, home_url, about_url,'/']
        
#         if not request.session.get('current_user_id') and not request.session.get('current_subuser_id'):
#             # User is not authenticated if neither session variable is set
#             if request.path not in excluded_paths and not request.path.startswith('/admin/'):
#                 # Exclude login, signup, home, about, and admin paths if needed
#                 return redirect(login_url)  # Redirect to the login page



from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class SessionExpiryMiddleware(MiddlewareMixin):
    def process_request(self, request):
        login_url = reverse('login')  # Get the URL for the login page
        signup_url = reverse('signup')  # Get the URL for the signup page
        home_url = reverse('home')  # Get the URL for the home page
        about_url = reverse('about')  # Get the URL for the about page
        services = reverse('services')  # Get the URL for the services page
        contact = reverse('contact')  # Get the URL for the contact page
        products = reverse('products')  # Get the URL for the products page

        


        # Define a list of paths to exclude from session check
        excluded_paths = [login_url, signup_url, home_url, about_url,services,contact,products,'/']
        
        if not request.session.get('current_user_id') and not request.session.get('current_subuser_id'):
            # User is not authenticated if neither session variable is set
            if request.path not in excluded_paths and not request.path.startswith('/admin'):
                # Exclude login, signup, home, about, and admin paths if needed
                return redirect(login_url)  # Redirect to the login page



# # myapp/middleware.py
# from django.shortcuts import redirect
# from .context_processors import custom_user, custom_subuser

# class LoginRedirectMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         context_user = custom_user(request)
#         context_subuser = custom_subuser(request)

#         if request.path in ['/', '/login'] and (context_user['current_user'] or context_subuser['current_subuser']):
#             return redirect('/admin_dashboard')
        
#         response = self.get_response(request)
#         return response

# myapp/middleware.py
from django.shortcuts import redirect
from .context_processors import custom_user, custom_subuser

class LoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        context_user = custom_user(request)
        context_subuser = custom_subuser(request)

        if request.path in ['/', '/login']:
            if context_user['current_user']:
                user = context_user['current_user']
                if user.user_type == 'super_admin':
                    return redirect('/super_admin_dashboard')
                elif user.user_type == 'admin':
                    return redirect('/admin_dashboard')
            elif context_subuser['current_subuser']:
                subuser = context_subuser['current_subuser']
                if subuser.user_type == 'editor':
                    return redirect('/editor_dashboard')
        
        response = self.get_response(request)
        return response



