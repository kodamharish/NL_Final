# context_processors.py
from .models import *

def custom_user(request):
    user_id = request.session.get('current_user_id')
    if user_id:
        try:
            user = User.objects.get(user_id=user_id)
            return {'current_user': user}
        except User.DoesNotExist:
            pass
    return {'current_user': None}

def custom_subuser(request):
    subuser_id = request.session.get('current_subuser_id')
    if subuser_id:
        try:
            subuser = Team.objects.get(subuser_id=subuser_id)
            return {'current_subuser': subuser}
        except Team.DoesNotExist:
            pass
    return {'current_subuser': None}

# def getAllCompanies(request):
#     user_context = custom_user(request)
#     current_user = user_context.get('current_user')

#     subuser_context = custom_subuser(request)
#     current_subuser = subuser_context.get('current_subuser')
    
#     if current_user:
#         current_user_companies = Company.objects.filter(user_id=current_user.user_id)
#         return {'current_user_companies':current_user_companies}
    
    
#     if current_subuser:
#         current_user_companies = Company.objects.filter(company_id=current_subuser.company_id)
#         return {'current_user_companies':current_user_companies}
#     else:
#         return {'current_user_companies':None}

# def getAllCompanies(request):
#     user_context = custom_user(request)
#     current_user = user_context.get('current_user')

#     subuser_context = custom_subuser(request)
#     current_subuser = subuser_context.get('current_subuser')
    
#     current_user_companies = None
#     current_user_company_profiles = None
#     company_profile_ids = []

#     if current_user:
#         # Retrieve companies associated with the current user
#         current_user_companies = Company.objects.filter(user_id=current_user.user_id)
        
#         # Retrieve company profiles associated with the current user's companies
#         if current_user_companies.exists():
#             company_ids = current_user_companies.values_list('company_id', flat=True)
#             current_user_company_profiles = CompanyProfile.objects.filter(company_id__in=company_ids)
#             company_profile_ids = list(current_user_company_profiles.values_list('company_id', flat=True))
            
        
#         return {
#             'current_user_companies': current_user_companies,
#             'current_user_company_profiles': current_user_company_profiles,
#             'company_profile_ids': company_profile_ids,
#             'company_ids':company_ids
#         }
    
#     if current_subuser:
#         # Retrieve companies associated with the current subuser
#         current_user_companies = Company.objects.filter(company_id=current_subuser.company_id)
#         return {'current_user_companies': current_user_companies}

#     return {'current_user_companies': None}


def getAllCompanies(request):
    user_context = custom_user(request)
    current_user = user_context.get('current_user')

    subuser_context = custom_subuser(request)
    current_subuser = subuser_context.get('current_subuser')
    
    current_user_companies = None
    current_user_company_profiles = None
    company_profile_ids = []
    first_company_id = None  # Variable to store the first company ID

    if current_user:
        # Retrieve companies associated with the current user
        current_user_companies = Company.objects.filter(user_id=current_user.user_id)
        
        # Retrieve company profiles associated with the current user's companies
        if current_user_companies.exists():
            company_ids = current_user_companies.values_list('company_id', flat=True)
            current_user_company_profiles = CompanyProfile.objects.filter(company_id__in=company_ids)
            company_profile_ids = list(current_user_company_profiles.values_list('company_id', flat=True))

            # Convert company_ids to a list and get the first value
            company_ids_list = list(company_ids)
            if company_ids_list:
                first_company_id = company_ids_list[0]
        
        return {
            'current_user_companies': current_user_companies,
            'current_user_company_profiles': current_user_company_profiles,
            'company_profile_ids': company_profile_ids,
            'company_ids': company_ids_list,
            'first_company_id': first_company_id
        }
    
    if current_subuser:
        # Retrieve companies associated with the current subuser
        current_user_companies = Company.objects.filter(company_id=current_subuser.company_id)
        return {'current_user_companies': current_user_companies}

    return {'current_user_companies': None}