from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
  path(''       , views.index,  name='index'),
]


from django.urls import path
from . import views
from .views import form_view, get_beds, get_varieties,data_table
from django.contrib.auth import views as auth_views
from .views import submit_week_entry, week_entries, user_entries_list, edit_entry

urlpatterns = [
    # path('', views.user_login, name='login'),
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/signin.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.week_form, name='week_form'),
    path('week-entry/', views.week_entry_form, name='week_entry_form'), 
    path('get_beds/', get_beds, name='get_beds'),
    path('get_varieties/', get_varieties, name='get_varieties'),  
    path('submit_week_entry/', views.submit_week_entry, name='submit_week_entry'),
    path('data_table/', data_table, name='data_table'),
    path("submit_week_entry/", submit_week_entry, name="submit_week_entry"),
    path("week_entries/", week_entries, name="week_entries"),

    path("my-entries/", user_entries_list, name="user_entries_list"),
    path("edit-entry/<int:entry_id>/", edit_entry, name="edit_entry"),
    path('get-entry-data/<int:entry_id>/', views.get_entry_data, name='get_entry_data'),
    path('edit-entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),

     path('get_bed_and_bay_for_variety/', views.get_bed_and_bay_for_variety, name='get_bed_and_bay_for_variety'),
     path('get_variety_suggestions/', views.get_variety_suggestions, name='get_variety_suggestions'),

     path('entries/<int:pk>/edit/', views.edit_entry_modal, name='edit_entry_modal'),
     path('entries/user/<int:user_id>/history/', views.user_entry_history, name='user_entry_history'),
]
