from django.db import models
from django.contrib.auth.hashers import make_password,is_password_usable


# Create your models here.
class UserIDSequence(models.Model):
    current_id = models.IntegerField(default=0)
    def __str__(self):
        return str(self.current_id)
    
class CompanyIDSequence(models.Model):
    current_id = models.IntegerField(default=0)
    def __str__(self):
        return str(self.current_id)
    
class SubUserIDSequence(models.Model):
    current_id = models.IntegerField(default=0)
    def __str__(self):
        return str(self.current_id)

class User(models.Model):
    user_id = models.CharField(max_length=10, primary_key=True, editable=False)
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(null=False)
    phone_number = models.IntegerField(null=True)
    linkedin_url = models.CharField(max_length=100,null=True)
    firstname = models.CharField(max_length=50,null=False)  
    lastname = models.CharField(max_length=50,null=True)
    password = models.CharField(max_length=500,null=False)  
    user_type = models.CharField(max_length=12,default='admin')
    company_type = models.CharField(max_length=20)
    email_verified=models.BooleanField(null=True, default=False)

    def save(self, *args, **kwargs):
        if not self.user_id:
            user_sequence, created = UserIDSequence.objects.get_or_create(pk=1)
            user_sequence.current_id += 1
            self.user_id = f'NL{user_sequence.current_id:03d}'
            user_sequence.save()
        # if self.password:
        #     # Hash the password
        #     self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)
    def __str__(self):
        return self.user_id
    
class Company(models.Model):
    # Company Details
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name='companies')
    company_id = models.CharField(max_length=10, primary_key=True, editable=False)
    name = models.CharField(max_length=100, null=True)
    date_of_incorporation = models.CharField(max_length=5, null=True)
    email = models.EmailField(null=True)
    phone=models.IntegerField(null=True)
    website_url = models.CharField(max_length=100,null=True)
    linkedin_url = models.CharField(max_length=100,null=True)   
    business_type = models.CharField(max_length=255, null=True)
    sector = models.CharField(max_length=255, null=True)
    company_type = models.CharField(max_length=10, null=True)
    location = models.CharField(max_length=20, null=True)
    no_of_employees=models.IntegerField(null=True)
    products=models.CharField(max_length=255, null=True)
    competitor=models.CharField(max_length=255, null=True)
    vision=models.CharField(max_length=255, null=True)
    customers=models.IntegerField(null=True)
    current_revenue=models.DecimalField(decimal_places=2, max_digits=25, null=True)
    current_pl=models.DecimalField(decimal_places=2, max_digits=25, null=True)
    previous_revenue=models.DecimalField(decimal_places=2, max_digits=25, null=True)
    previous_pl=models.DecimalField(decimal_places=2, max_digits=25, null=True)
    a_yearbefore_revenue=models.DecimalField(decimal_places=2, max_digits=25, null=True)
    a_yearbefore_pl=models.DecimalField(decimal_places=2, max_digits=25, null=True)
    additional=models.TextField(null=True)
    subscription_type = models.CharField(max_length=10, null=True)


    def save(self, *args, **kwargs):
        if not self.company_id:
            company_sequence, created = CompanyIDSequence.objects.get_or_create(pk=1)
            company_sequence.current_id += 1
            self.company_id = f'C{company_sequence.current_id:03d}'
            company_sequence.save()
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.company_id

class CompanyProfile(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='company_profiles')
    tam = models.FloatField()
    cagr = models.FloatField()
    number_of_clients_users = models.IntegerField()
    previous_year_revenue = models.FloatField()
    current_year_revenue_arr = models.FloatField()
    current_monthly_burn_rate = models.FloatField()
    forecasted_revenue_for_next_year = models.FloatField()
    business_stage = models.ForeignKey('BusinessStage', on_delete=models.CASCADE)
    equity_funds_raised_so_far = models.FloatField()
    funds_needed = models.FloatField()
    business_plan = models.FileField(upload_to='business_plan',null=True)
    pitch_video = models.FileField(upload_to='pitch',null=True)
    product_video = models.FileField(upload_to='product',null=True)

class Ask(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    ask=models.IntegerField(null=True)
    valuation=models.IntegerField(null=True)
    equity_share=models.DecimalField(decimal_places=1, null=True, max_digits=5)
    details=models.TextField()
    

class Sector(models.Model):
    #company_id=models.ForeignKey(Company, on_delete=models.CASCADE,related_name='sectors')
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name

class BusinessType(models.Model):
    #company_id=models.ForeignKey(Company, on_delete=models.CASCADE,related_name='business_types')
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class BusinessStage(models.Model):
    #company_id=models.ForeignKey(Company, on_delete=models.CASCADE,related_name='business_stages')
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Founder(models.Model):
    company_id=models.ForeignKey(Company, on_delete=models.CASCADE,related_name='founders')
    name=models.CharField(max_length=50)
    linkedin_url=models.CharField(max_length=100,null=True)
    short_profile=models.TextField(null=True)
    photo=models.ImageField(upload_to='founder_photos',null=True)
    title=models.CharField(null=True, max_length=20)
    date_joined=models.DateField(null=True)
    def __str__(self):
        return self.name

class ExecutiveMember(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='executive_members')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    designation = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Advisor(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='advisors')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phonenumber = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Challenge(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='challenges')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class SolvedProblem(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='solved_problems')
    description = models.TextField()

    def __str__(self):
        return self.description

class Competitor(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='competitors')
    name = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name



class SocialMedia(models.Model):
    company_id=models.ForeignKey(Company,on_delete=models.CASCADE,related_name='social_media_urls')
    #name=models.CharField(max_length=25)
    url=models.CharField(max_length=100,null=True)

class Client(models.Model):
    company_id=models.ForeignKey(Company, on_delete=models.CASCADE,related_name='clients')
    name=models.CharField(max_length=25)
    logo=models.ImageField(upload_to='clients_logo',null=True)

class CapTable(models.Model):
    company_id=models.ForeignKey(Company, on_delete=models.CASCADE,related_name='cap_tables')
    name = models.CharField(max_length=200)
    shareholder=models.CharField(max_length=50, null=True)
    percentage_of_shares= models.DecimalField(max_digits=5,decimal_places=2)
    investedsince=models.DateField(null=True)
    amount=models.IntegerField(null=True)
    valuation=models.IntegerField(null=True)
    details=models.TextField(null=True)




class Team(models.Model):
    subuser_id = models.CharField(max_length=10, primary_key=True)
    #creator_id = models.ForeignKey(User,on_delete=models.CASCADE)
    creator_id = models.CharField(max_length=15)
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(null=False)
    phone_number = models.IntegerField(null=False)
    linkedin_url = models.CharField(max_length=100,null=True)
    firstname = models.CharField(max_length=50,null=False)
    lastname = models.CharField(max_length=50,null=True)
    password = models.CharField(max_length=10,null=False)  
    user_type = models.CharField(max_length=12)

    def save(self, *args, **kwargs):
        if not self.subuser_id:
            subuser_sequence, created = SubUserIDSequence.objects.get_or_create(pk=1)
            subuser_sequence.current_id += 1
            self.subuser_id = f'SUBNL{subuser_sequence.current_id:03d}'
            subuser_sequence.save()
        if self.password:
            # Hash the password
            self.password = make_password(self.password)
        super(Team, self).save(*args, **kwargs)
    def __str__(self):
        return self.subuser_id

class productsandservices(models.Model):
    company_id=models.ForeignKey(Company, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    launch_date=models.DateField()
    description=models.TextField()
    industry=models.CharField(max_length=100)
    type_of_business=models.CharField(max_length=100)
    problem_solved=models.TextField()
    current_year_revenue=models.IntegerField()
    previous_year_revenue=models.IntegerField()
    a_year_before_revenue=models.IntegerField()
    current_year_pl=models.IntegerField()
    previous_year_pl=models.IntegerField()
    a_year_before_pl=models.IntegerField()
    customers=models.TextField()
    competitors=models.TextField()
    




class IncomeStatement(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    end_date = models.DateField(null=True)

    # All fields now have a default value of 0
    total_revenue = models.IntegerField(default=0, null=True)
    operating_revenue = models.IntegerField(default=0, null=True)
    cost_of_revenue = models.IntegerField(default=0, null=True)
    gross_profit = models.IntegerField(default=0, null=True)
    operating_expense = models.IntegerField(default=0, null=True)
    selling_general_and_administrative_expense = models.IntegerField(default=0, null=True)
    general_and_administrative_expenses = models.IntegerField(default=0, null=True)
    selling_and_marketing_expense = models.IntegerField(default=0, null=True)
    research_and_development_expense = models.IntegerField(default=0, null=True)
    operating_income = models.IntegerField(default=0, null=True)
    net_non_operating_interest_income_expense = models.IntegerField(default=0, null=True)
    interest_income_non_operating = models.IntegerField(default=0, null=True)
    interest_expense_non_operating = models.IntegerField(default=0, null=True)
    other_income_or_expense = models.IntegerField(default=0, null=True)
    gain_or_loss_on_sale_of_security = models.IntegerField(default=0, null=True)
    special_income_or_charges = models.IntegerField(default=0, null=True)
    write_off = models.IntegerField(default=0, null=True)
    other_non_operating_income_or_expenses = models.IntegerField(default=0, null=True)
    pretax_income = models.IntegerField(default=0, null=True)
    tax_provision = models.IntegerField(default=0, null=True)
    net_income = models.IntegerField(default=0, null=True)
    preference_share_dividends = models.IntegerField(default=0, null=True)
    net_income_to_common_stockholders = models.IntegerField(default=0, null=True)
    equity_share_dividends = models.IntegerField(default=0, null=True)
    retained_earnings = models.IntegerField(default=0, null=True)
    basic_eps = models.DecimalField(default=0.00, null=True, max_digits=12, decimal_places=2)
    diluted_eps = models.IntegerField(default=0, null=True)
    depreciation_and_amortization = models.IntegerField(default=0, null=True)
    ebitda = models.IntegerField(default=0, null=True)
    no_of_equity_shares = models.IntegerField(default=0, null=True)
    
    monthly_or_quarterly_or_yearly = models.CharField(max_length=15, null=True)
    month_or_quarter_or_year_name = models.CharField(max_length=15, null=True)


    creator_id = models.IntegerField(default=0, null=True)
    modifier_id = models.IntegerField(default=0, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)



class BalanceSheet(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    end_date = models.DateField(null=True)

    # All fields now have a default value of 0
    total_assets = models.IntegerField(default=0, null=True)
    current_assets = models.IntegerField(default=0, null=True)
    cash_cash_equivalents_and_short_term_investments = models.IntegerField(default=0, null=True)
    cash_and_cash_equivalents = models.IntegerField(default=0, null=True)
    cash = models.IntegerField(default=0, null=True)
    cash_equivalents = models.IntegerField(default=0, null=True)
    other_short_term_investments = models.IntegerField(default=0, null=True)
    receivables = models.IntegerField(default=0, null=True)
    accounts_receivable = models.IntegerField(default=0, null=True)
    gross_accounts_receivable = models.IntegerField(default=0, null=True)
    allowance_for_doubtful_accounts_receivable = models.IntegerField(default=0, null=True)
    other_receivables = models.IntegerField(default=0, null=True)
    inventory = models.IntegerField(default=0, null=True)
    raw_materials = models.IntegerField(default=0, null=True)
    work_in_process = models.IntegerField(default=0, null=True)
    finished_goods = models.IntegerField(default=0, null=True)
    hedging_current_assets = models.IntegerField(default=0, null=True)
    other_current_assets = models.IntegerField(default=0, null=True)
    total_non_current_assets = models.IntegerField(default=0, null=True)
    net_ppe = models.IntegerField(default=0, null=True)
    gross_ppe = models.IntegerField(default=0, null=True)
    land_and_improvements = models.IntegerField(default=0, null=True)
    buildings_and_improvements = models.IntegerField(default=0, null=True)
    machinery_furniture_equipment = models.IntegerField(default=0, null=True)
    other_properties = models.IntegerField(default=0, null=True)
    leases = models.IntegerField(default=0, null=True)
    accumulated_depreciation = models.IntegerField(default=0, null=True)
    goodwill_and_other_intangible_assets = models.IntegerField(default=0, null=True)
    goodwill = models.IntegerField(default=0, null=True)
    other_intangible_assets = models.IntegerField(default=0, null=True)
    investments_and_advances = models.IntegerField(default=0, null=True)
    long_term_equity_investment = models.IntegerField(default=0, null=True)
    other_non_current_assets = models.IntegerField(default=0, null=True)
    total_liabilities_net_minority_interest = models.IntegerField(default=0, null=True)
    current_liabilities = models.IntegerField(default=0, null=True)
    payables_and_accrued_expenses = models.IntegerField(default=0, null=True)
    accounts_payable = models.IntegerField(default=0, null=True)
    income_tax_payable = models.IntegerField(default=0, null=True)
    pension_and_other_post_retirement_benefit_plans_current = models.IntegerField(default=0, null=True)
    current_debt_and_capital_lease_obligation = models.IntegerField(default=0, null=True)
    current_debt = models.IntegerField(default=0, null=True)
    capital_lease_obligation = models.IntegerField(default=0, null=True)
    current_deferred_liabilities = models.IntegerField(default=0, null=True)
    current_deferred_revenue = models.IntegerField(default=0, null=True)
    other_current_liabilities = models.IntegerField(default=0, null=True)
    total_non_current_liabilities_net_minority_interest = models.IntegerField(default=0, null=True)
    long_term_debt_and_capital_lease_obligation = models.IntegerField(default=0, null=True)
    long_term_debt = models.IntegerField(default=0, null=True)
    long_term_capital_lease_obligation = models.IntegerField(default=0, null=True)
    non_current_deferred_liabilities = models.IntegerField(default=0, null=True)
    non_current_deferred_taxes_liabilities = models.IntegerField(default=0, null=True)
    non_current_deferred_revenue = models.IntegerField(default=0, null=True)
    trade_and_other_payables_non_current = models.IntegerField(default=0, null=True)
    other_non_current_liabilities = models.IntegerField(default=0, null=True)
    total_equity_gross_minority_interest = models.IntegerField(default=0, null=True)
    stockholders_equity = models.IntegerField(default=0, null=True)
    capital_stock = models.IntegerField(default=0, null=True)
    common_stock = models.IntegerField(default=0, null=True)
    retained_earnings = models.IntegerField(default=0, null=True)
    gains_or_losses_not_affecting_retained_earnings = models.IntegerField(default=0, null=True)
    other_equity_adjustments = models.IntegerField(default=0, null=True)

    # Other fields
    monthly_or_quarterly_or_yearly = models.CharField(max_length=15, null=True)
    month_or_quarter_or_year_name = models.CharField(max_length=15, null=True)

    creator_id = models.CharField( max_length=35, null=True)
    modifier_id = models.CharField( max_length=35, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)




class CashFlow(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    end_date = models.DateField(null=True)

    # All fields now have a default value of 0
    operating_cash_flow = models.IntegerField(default=0, null=True)
    net_income_from_continuing_operations = models.IntegerField(default=0, null=True)
    depreciation_and_amortization = models.IntegerField(default=0, null=True)
    change_in_working_capital = models.IntegerField(default=0, null=True)
    changes_in_receivables = models.IntegerField(default=0, null=True)
    change_in_inventory = models.IntegerField(default=0, null=True)
    change_in_hedging_assets_current = models.IntegerField(default=0, null=True)
    change_in_other_current_assets = models.IntegerField(default=0, null=True)
    change_in_payables_and_accrued_expense = models.IntegerField(default=0, null=True)
    change_in_pension_and_other_post_retirement_benefit_plans_current = models.IntegerField(default=0, null=True)
    change_in_current_debt_and_capital_lease_obligation = models.IntegerField(default=0, null=True)
    change_in_current_deferred_liabilities = models.IntegerField(default=0, null=True)
    change_in_other_current_liabilities = models.IntegerField(default=0, null=True)
    investing_cash_flow = models.IntegerField(default=0, null=True)
    cash_flow_from_continuing_investing_activities = models.IntegerField(default=0, null=True)
    net_ppe_purchase_and_sale = models.IntegerField(default=0, null=True)
    goodwill_and_other_intangible_assets = models.IntegerField(default=0, null=True)
    investments_and_advances = models.IntegerField(default=0, null=True)
    other_non_current_assets = models.IntegerField(default=0, null=True)
    financing_cash_flow = models.IntegerField(default=0, null=True)
    cash_flow_from_continuing_financing_activities = models.IntegerField(default=0, null=True)
    long_term_debt_and_capital_lease_obligation = models.IntegerField(default=0, null=True)
    non_current_deferred_liabilities = models.IntegerField(default=0, null=True)
    trade_and_other_payables_non_current = models.IntegerField(default=0, null=True)
    other_non_current_liabilities = models.IntegerField(default=0, null=True)
    common_stock_issuance_payments = models.IntegerField(default=0, null=True)
    common_stock_dividend_paid = models.IntegerField(default=0, null=True)
    end_cash_position = models.IntegerField(default=0, null=True)
    changes_in_cash = models.IntegerField(default=0, null=True)
    beginning_cash_position = models.IntegerField(default=0, null=True)
    capital_expenditure = models.IntegerField(default=0, null=True)
    issuance_repurchase_of_capital_stock = models.IntegerField(default=0, null=True)
    repayment_of_debt = models.IntegerField(default=0, null=True)
    free_cash_flow = models.IntegerField(default=0, null=True)

    # Other fields
    monthly_or_quarterly_or_yearly = models.CharField(max_length=15, null=True)
    month_or_quarter_or_year_name = models.CharField(max_length=15, null=True)

    creator_id = models.CharField(max_length=15, null=True)
    modifier_id = models.CharField(max_length=15, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)




class BalanceSheetRatios(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    balancesheet = models.ForeignKey(BalanceSheet, on_delete=models.CASCADE)
    current_ratio = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    quick_ratio = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    cash_ratio = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    working_capital = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    debt_equity_ratio = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    debt_ratio = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    equity_ratio = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    debt_capital_ratio = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    operating_cash_flow_ratio = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    debt_service_coverage_ratio = models.DecimalField(max_digits=25, decimal_places=2, null=True)

class IncomeStatementRatios(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    incomesheet = models.ForeignKey(IncomeStatement, on_delete=models.CASCADE)
    gross_profit_ratio = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    operating_profit_ratio = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    ebitda_margin = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    net_profit_margin = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    earnings_per_share = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    interest_service = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    operating_cash_flow_ratio = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    debt_service_coverage_ratio = models.DecimalField(max_digits=25, decimal_places=2, null=True)

class CashFlowRatios(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    cashflowsheet = models.ForeignKey(CashFlow, on_delete=models.CASCADE)
    current_ratio = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    quick_ratio = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    cash_ratio = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    working_capital = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    operating_cash_flow_ratio = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    debt_service_coverage_ratio = models.DecimalField(max_digits=25, decimal_places=2, null=True)




    
class Company_news(models.Model):
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)  
    sub_date = models.DateField(default=None, null=True)
    line_no = models.IntegerField(default=None, null=True)  
    summary = models.TextField()
    link = models.CharField(max_length=50, default=None, null=True)




class plan_finacials(models.Model):
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)  
    line_no = models.IntegerField(default=None, null=True)  
    b_plan_pdf = models.FileField(upload_to='plan_pdf',null=True)
    f_plan_pdf = models.FileField(upload_to='f_plan_pdf',null=True)
    p_name=models.CharField(max_length=50, default=None, null=True)


class companypptandvideo(models.Model):
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)  
    line_no = models.IntegerField(default=None, null=True)  
    ppt_file = models.FileField(upload_to='ppt_file_f',null=True)
    video_file = models.FileField(upload_to='video_file_f',null=True)
    p_name=models.CharField(max_length=50, default=None, null=True)


class BenchMark(models.Model):
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)  
    line_no = models.IntegerField(default=None, null=True)  
    valuation = models.BigIntegerField(null=True)
    source = models.CharField(max_length=100, null=True)
    valuation_dt = models.DateField(null=True)    
    valuation_doc = models.FileField(upload_to='BenchMark',null=True)
    bench_mark_doc = models.FileField(upload_to='BenchMark',null=True)
    p_name=models.CharField(max_length=50, default=None, null=True)



class ForecastingIncomeStatement(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    total_revenue = models.JSONField(default=dict)
    operating_revenue = models.JSONField(default=dict)
    cost_of_revenue = models.JSONField(default=dict)
    gross_profit = models.JSONField(default=dict)
    operating_expense = models.JSONField(default=dict)
    selling_general_and_administrative_expense = models.JSONField(default=dict)
    general_and_administrative_expenses = models.JSONField(default=dict)
    selling_and_marketing_expense = models.JSONField(default=dict)
    research_and_development_expense = models.JSONField(default=dict)
    operating_income = models.JSONField(default=dict)
    net_non_operating_interest_income_expense = models.JSONField(default=dict)
    interest_income_non_operating = models.JSONField(default=dict)
    interest_expense_non_operating = models.JSONField(default=dict)
    other_income_or_expense = models.JSONField(default=dict)
    gain_or_loss_on_sale_of_security = models.JSONField(default=dict)
    special_income_or_charges = models.JSONField(default=dict)
    write_off = models.JSONField(default=dict)
    other_non_operating_income_or_expenses = models.JSONField(default=dict)
    pretax_income = models.JSONField(default=dict)
    tax_provision = models.JSONField(default=dict)
    net_income = models.JSONField(default=dict)
    preference_share_dividends = models.JSONField(default=dict)
    net_income_to_common_stockholders = models.JSONField(default=dict)
    equity_share_dividends = models.JSONField(default=dict)
    retained_earnings = models.JSONField(default=dict)
    basic_eps = models.JSONField(default=dict)
    diluted_eps = models.JSONField(default=dict)
    depreciation_and_amortization = models.JSONField(default=dict)
    ebitda = models.JSONField(default=dict)
    no_of_equity_shares = models.JSONField(default=dict)
    
    monthly_or_quarterly_or_yearly = models.CharField(max_length=15, null=True)
    month_or_quarter_or_year_name = models.CharField(max_length=15, null=True)


    




class ForecastingBalanceSheet(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    total_assets = models.JSONField(default=dict)
    current_assets = models.JSONField(default=dict)
    cash_cash_equivalents_and_short_term_investments = models.JSONField(default=dict)
    cash_and_cash_equivalents = models.JSONField(default=dict)
    cash = models.JSONField(default=dict)
    cash_equivalents = models.JSONField(default=dict)
    other_short_term_investments = models.JSONField(default=dict)
    receivables = models.JSONField(default=dict)
    accounts_receivable = models.JSONField(default=dict)
    gross_accounts_receivable = models.JSONField(default=dict)
    allowance_for_doubtful_accounts_receivable = models.JSONField(default=dict)
    other_receivables = models.JSONField(default=dict)
    inventory = models.JSONField(default=dict)
    raw_materials = models.JSONField(default=dict)
    work_in_process = models.JSONField(default=dict)
    finished_goods =models.JSONField(default=dict)
    hedging_current_assets = models.JSONField(default=dict)
    other_current_assets = models.JSONField(default=dict)
    total_non_current_assets = models.JSONField(default=dict)
    net_ppe = models.JSONField(default=dict)
    gross_ppe = models.JSONField(default=dict)
    land_and_improvements = models.JSONField(default=dict)
    buildings_and_improvements = models.JSONField(default=dict)
    machinery_furniture_equipment = models.JSONField(default=dict)
    other_properties = models.JSONField(default=dict)
    leases = models.JSONField(default=dict)
    accumulated_depreciation = models.JSONField(default=dict)
    goodwill_and_other_intangible_assets = models.JSONField(default=dict)
    goodwill = models.JSONField(default=dict)
    other_intangible_assets = models.JSONField(default=dict)
    investments_and_advances = models.JSONField(default=dict)
    long_term_equity_investment = models.JSONField(default=dict)
    other_non_current_assets = models.JSONField(default=dict)
    total_liabilities_net_minority_interest = models.JSONField(default=dict)
    current_liabilities = models.JSONField(default=dict)
    payables_and_accrued_expenses = models.JSONField(default=dict)
    accounts_payable = models.JSONField(default=dict)
    income_tax_payable = models.JSONField(default=dict)
    pension_and_other_post_retirement_benefit_plans_current = models.JSONField(default=dict)
    current_debt_and_capital_lease_obligation = models.JSONField(default=dict)
    current_debt = models.JSONField(default=dict)
    capital_lease_obligation = models.JSONField(default=dict)
    current_deferred_liabilities = models.JSONField(default=dict)
    current_deferred_revenue = models.JSONField(default=dict)
    other_current_liabilities = models.JSONField(default=dict)
    total_non_current_liabilities_net_minority_interest = models.JSONField(default=dict)
    long_term_debt_and_capital_lease_obligation = models.JSONField(default=dict)
    long_term_debt = models.JSONField(default=dict)
    long_term_capital_lease_obligation = models.JSONField(default=dict)
    non_current_deferred_liabilities =models.JSONField(default=dict)
    non_current_deferred_taxes_liabilities = models.JSONField(default=dict)
    non_current_deferred_revenue = models.JSONField(default=dict)
    trade_and_other_payables_non_current = models.JSONField(default=dict)
    other_non_current_liabilities = models.JSONField(default=dict)
    total_equity_gross_minority_interest = models.JSONField(default=dict)
    stockholders_equity = models.JSONField(default=dict)
    capital_stock = models.JSONField(default=dict)
    common_stock = models.JSONField(default=dict)
    retained_earnings = models.JSONField(default=dict)
    gains_or_losses_not_affecting_retained_earnings = models.JSONField(default=dict)
    other_equity_adjustments = models.JSONField(default=dict)

    # Other fields
    monthly_or_quarterly_or_yearly = models.CharField(max_length=15, null=True)
    month_or_quarter_or_year_name = models.CharField(max_length=15, null=True)

    

class ForecastingCashFlow(models.Model):
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
    operating_cash_flow = models.JSONField(default=dict)
    net_income_from_continuing_operations = models.JSONField(default=dict)
    depreciation_and_amortization = models.JSONField(default=dict)
    change_in_working_capital = models.JSONField(default=dict)
    changes_in_receivables = models.JSONField(default=dict)
    change_in_inventory = models.JSONField(default=dict)
    change_in_hedging_assets_current = models.JSONField(default=dict)
    change_in_other_current_assets = models.JSONField(default=dict)
    change_in_payables_and_accrued_expense = models.JSONField(default=dict)
    change_in_pension_and_other_post_retirement_benefit_plans_current = models.JSONField(default=dict)
    change_in_current_debt_and_capital_lease_obligation = models.JSONField(default=dict)
    change_in_current_deferred_liabilities = models.JSONField(default=dict)
    change_in_other_current_liabilities = models.JSONField(default=dict)
    investing_cash_flow = models.JSONField(default=dict)
    cash_flow_from_continuing_investing_activities = models.JSONField(default=dict)
    net_ppe_purchase_and_sale = models.JSONField(default=dict)
    goodwill_and_other_intangible_assets = models.JSONField(default=dict)
    investments_and_advances = models.JSONField(default=dict)
    other_non_current_assets = models.JSONField(default=dict)
    financing_cash_flow = models.JSONField(default=dict)
    cash_flow_from_continuing_financing_activities = models.JSONField(default=dict)
    long_term_debt_and_capital_lease_obligation = models.JSONField(default=dict)
    non_current_deferred_liabilities = models.JSONField(default=dict)
    trade_and_other_payables_non_current = models.JSONField(default=dict)
    other_non_current_liabilities = models.JSONField(default=dict)
    common_stock_issuance_payments = models.JSONField(default=dict)
    common_stock_dividend_paid = models.JSONField(default=dict)
    end_cash_position = models.JSONField(default=dict)
    changes_in_cash = models.JSONField(default=dict)
    beginning_cash_position = models.JSONField(default=dict)
    capital_expenditure = models.JSONField(default=dict)
    issuance_repurchase_of_capital_stock = models.JSONField(default=dict)
    repayment_of_debt = models.JSONField(default=dict)
    free_cash_flow = models.JSONField(default=dict)
    monthly_or_quarterly_or_yearly = models.CharField(max_length=15, null=True)
    month_or_quarter_or_year_name = models.CharField(max_length=15, null=True)



