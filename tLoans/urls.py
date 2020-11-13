from django.urls import path
from .import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('short-term/', views.ShortTerm.as_view(), name='short-term'),
    path('long-term/', views.LongTerm.as_view(), name='long-term'),
    path('savings/add/', views.AddSavings.as_view(), name='add-saving'),
    path('savings/remove', views.DeductSaving.as_view(), name='remove-saving'),
    path('loan/information/', views.LoanInformation.as_view(), name='loan_information'),
    path('boosters/', views.SaveBooster.as_view(), name='save_booster'),



    # delete short term
    path('delete/short-term/<int:pk>/', views.DeleteShortTermLoan.as_view(), name='delete-short-term'),
    # delete long term
    path('delete/long-term/<int:pk>/', views.DeleteLongTermLoan.as_view(), name='delete-long-term'),
    # delete long term amount
    path('delete/long-term-amount/<int:pk>/', views.DeleteLongTermPayment.as_view(), name='delete-long-term-amount')

]