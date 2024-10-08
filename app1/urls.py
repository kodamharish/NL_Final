from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL 
    path('',home,name='home'), # Home URL
    path('home',home,name='home'),
    path('about',about,name='about'),
    path('services',services,name='services'),
    path('contact',contact,name='contact'),
    path('products',products_page, name='products'),
    #login,logout
    path('login',login,name='login'),
    path('logout',logout,name='logout'),
    #path('sign_up',signup,name='sign_up'),
    path('signup',signup,name='signup'),

    #path('investor_sign_up',investorSignUp,name='investor_sign_up'),
    #path('ca_firm_sign_up',caFirmSignUp,name='ca_firm_sign_up'),

    #Super Admin
    path('super_admin_dashboard',superAdminDashboard,name='super_admin_dashboard'),
    path('admins',admins,name='admins'),
    path('editors',editors,name='editors'),
    path('users',users,name='users'),
    path('startups',startups,name='startups'),
    path('investors',investors,name='investors'),
    path('ca_firms',ca_firms,name='ca_firms'),
    path('companies',companies,name='companies'),


    #Admin
    #path('admin_dashboard/<str:id>/',adminDashboard,name='admin_dashboard'),
    path('admin_dashboard',adminDashboard,name='admin_dashboard'),

    
    #company
    path('add_company',addCompany,name='add_company'), 
    path('company_profile/<str:id>/',companyProfile,name='company_profile'),
    path('founders/<str:id>/', founders, name='founders'),

    path('basic_information/<str:id>/',basicInformation,name='basic_information'),


    path('business_plan/<str:id>/',businessPlan,name='business_plan'),
    path('news_post/<str:id>/',news_post,name='news_post'),
    path('pitch_and_product/<str:id>/',pitchAndProduct,name='pitch_and_product'),
    

    path('cap_table/<str:id>/',capTable,name='cap_table'),
    path('company_ask/<str:id>/', company_ask, name='company_ask'),


    path('income_statement/<str:id>/',incomeStatement,name='income_statement'), 
    path('balance_sheet/<str:id>/',balanceSheet,name='balance_sheet'), 
    path('cash_flow/<str:id>/',cashFlow,name='cash_flow'),
    

    
    #investor 
    path('investor_dashboard',investorDashboard,name='investor_dashboard'),
    path('investor_base/<str:id>/',investorBase,name='investor_base'),
    path('founders_and_team/<str:id>/',founderAndTeam,name='founders_and_team'),
   #Planning & Budgeting
    path('planning_budgeting_income_statement_table/<str:id>/',incomeStatementTable,name='planning_budgeting_income_statement_table'), 
    path('planning_budgeting_balance_sheet_table/<str:id>/',balanceSheetTable,name='planning_budgeting_balance_sheet_table'), 
    path('planning_budgeting_cash_flow_table/<str:id>/',cashFlowTable,name='planning_budgeting_cash_flow_table'),
    path('cash_flow_manual_entry/<str:id>/', cashflowmanualentry, name='cash_flow_manual_entry'),
    path('cashflowfirstyear/<str:id>/', cashflowfirstyearofoperations, name='cashflowfirstyearofoperations'),
    

    #Forecasting
    path('forecasting_income_statement_table/<str:id>/',forecastedIncomeStatementTable,name='forecasting_income_statement_table'),
    path('forecasting_balance_sheet_table/<str:id>/',forecastedBalanceSheetTable,name='forecasting_balance_sheet_table'),
    path('forecasting_cash_flow_table/<str:id>/',forecastedCashFlowTable,name='forecasting_cash_flow_table'),    

    path('forecasting_income_statement_table/<str:id>/',incomeStatementTable,name='forecasting_income_statement_table'),
    #path('forecasting_balance_sheet_table/<str:id>/',balanceSheetTable,name='forecasting_balance_sheet_table'), 
    #path('forecasting_cash_flow_table/<str:id>/',cashFlowTable,name='forecasting_cash_flow_table'), 

    # path('financial_statement/<str:id>/',financialStatement,name='financial_statement'),
    # path('revenue_verticals/<str:company_id>/',revenueVerticals,name='revenue_verticals'),
    # path('expenses/<str:company_id>/',expenses,name='expenses'),

    #children
    path('my_team',myTeam,name='my_team'),
    path('add_team',addTeam,name='add_team'),
    path('update_team/<str:id>',updateTeam,name='update_team'),
    path('delete_team/<str:id>',deleteTeam,name='delete_team'),

    path('parent',parent,name='parent'),
    #path('profit_loss_balance_sheet',profitLossBalanceSheetCalculation,name='profit_loss_balance_sheet'),

    #editor
    path('editor_dashboard',editorDashboard,name='editor_dashboard'),
    #user
    path('user_dashboard',userDashboard,name='user_dashboard'),

    #password reset
    path('forgot_password_1',forgotPasswordOne,name='forgot_password_1'),
    path('forgot_password_2',forgotPasswordTwo,name='forgot_password_2'),


    #edit url's
    # path('save_incomesataement/<str:id>/', save_incomestatement, name='save_income_statement'),
    path('save-edited-data/<str:company_id>/', save_edited_data, name='save_edited_data'),
    path('save-edited-data-income/<str:company_id>/', save_edited_data_income, name='save_edited_data_income'),

    path('delete-cap-table-entry/<int:id>/', delete_cap_table_entry, name='delete_cap_table_entry'),
    path('update-cap-table-entry/<int:id>/', update_cap_table_entry, name='update_cap_table_entry'),
    path('delete-ask-entry/<int:id>/', delete_ask_entry, name='delete_ask_entry'),
    path('company_ask/delete/<str:company_id>/<int:entry_id>/', delete_company_ask, name='delete_company_ask'),
    path('cap_table/<str:id>/',capTable,name='cap_table'),
    path('company_ask/<str:id>/', company_ask, name='company_ask'),
    path('company_ask/update/<str:company_id>/<int:entry_id>/', update_entry, name='update_entry'),
    path('company_ask/get/<int:entry_id>/', get_entry, name='get_entry'),
    path('founder/delete/<int:founder_id>/', delete_founder, name='delete_founder'),

    path('business_plan/<str:id>/',businessPlan,name='business_plan'),
    path('remove-file/', remove_file, name='remove_file'),
    path('news_post/<str:id>/',news_post,name='news_post'),
    path('pitchvideoandppt/<str:id>/',pitchvideoandppt,name='pitchvideoandppt'),
    path('pitchvideoandppt_remove/', pitchvideoandppt_remove, name='pitchvideoandppt_remove'), 
    path('bench4/<str:id>/', bench4, name='bench4'),
    path('bench4_files/<str:id>', bench4_files, name='bench4_files'),
    path('remove-bench4-file/', remove_bench4_file, name='remove_bench4_file'),
    path('delete_bench/<str:line_no>/', delete_bench, name='delete_bench'),

    path('activate-user/<uidb64>/<token>/', activate_user, name='activate'),
    path('news/delete/<int:news_id>/', delete_news, name='delete_news'),
    path('news/update/<int:line_no>/', update_news, name='update_news'),

]