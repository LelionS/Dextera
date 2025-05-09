from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout

from .models import *

def index(request):

  context = {
    'segment'  : 'index',
    #'products' : Product.objects.all()
  }
  return render(request, "pages/index.html", context)



from django.shortcuts import render, redirect
from .forms import WeekEntryForm
from django.http import HttpResponse
from .models import WeekEntry
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from .models import Bay, Bed, Variety

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required



@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def week_form(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'forms/week_form.html', {'user': request.user})
@login_required
def form_view(request):
    bays = Bay.objects.all()
    return render(request, 'forms/form.html', {'bays': bays})
@login_required
def get_beds(request):
    bay_id = request.GET.get('bay_id')
    beds = Bed.objects.filter(bay_id=bay_id).values('id', 'code')
    return JsonResponse({'beds': list(beds)})
@login_required
def get_varieties(request):
    bed_id = request.GET.get('bed_id')
    varieties = Variety.objects.filter(bed_id=bed_id).values('id', 'name')
    return JsonResponse({'varieties': list(varieties)})
@login_required
def week_entry_form(request):
    bays = Bay.objects.all()
    return render(request, 'week_entry_form.html', {'bays': bays})
@login_required
def fetch_beds(request):
    bay_id = request.GET.get('bay_id')
    beds = Bed.objects.filter(bay_id=bay_id).values('id', 'code')   
    return JsonResponse({'beds': list(beds)})
@login_required
def fetch_varieties(request):
    bed_id = request.GET.get('bed_id')
    varieties = Variety.objects.filter(bed_id=bed_id).values('id', 'name')   
    return JsonResponse({'varieties': list(varieties)})

@login_required
def submit_week_entry(request):
    if request.method == 'POST':
        week = request.POST.get('week')
        bed_no = request.POST.get('bed_no')
        variety = request.POST.get('variety')
        amounts = request.POST.get('amounts')

        if not all([week, bed_no, variety, amounts]):
            messages.error(request, "❌ Missing form data!")
            return redirect('week_entry_form')

        try:
            WeekEntry.objects.create(week=week, bed_no_id=bed_no, variety_id=variety, amounts=amounts)
            messages.success(request, "✅ Form submitted successfully!")
        except Exception as e:
            messages.error(request, f"❌ Error saving data: {e}")

        return redirect('forms/week_entry_form')

@login_required
def week_form(request):
    bays = Bay.objects.all()
    beds = Bed.objects.all()
    varieties = Variety.objects.all()

    context = {
        'bays': bays,
        'beds': beds,
        'varieties': varieties,
    }
    
    return render(request, 'forms/week_form.html', context)


# --------------------------------------------------------------------

from django.shortcuts import render
from .models import DataEntry

@login_required
def data_table(request):
    entries = DataEntry.objects.all()  # Fetch stored data
    print(entries)  # Debugging: Check if data is retrieved
    return render(request, 'data_table.html', {'entries': entries})
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import WeekEntry, Bay, Bed, Variety


from django.http import JsonResponse
from .models import Variety, WeekEntry
from django.views.decorators.http import require_POST

@require_POST
def submit_week_entry(request):
    try:
        variety_id = request.POST.get("variety")
        amounts = request.POST.get("amounts")
        week = request.POST.get("date")
        submitted_by_id = request.POST.get("submitted_by")

        if not all([variety_id, amounts, week, submitted_by_id]):
            return JsonResponse({"error": "Missing one or more required fields."}, status=400)

        variety = Variety.objects.get(id=variety_id)
        bed = variety.bed
        bay = bed.bay

        WeekEntry.objects.create(
            week=week,
            bay=bay,
            bed=bed,
            variety=variety,
            amounts=int(amounts),
            submitted_by_id=submitted_by_id,
        )

        return JsonResponse({"message": "Entry submitted successfully."})
    
    except Variety.DoesNotExist:
        return JsonResponse({"error": "Invalid variety selected."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)



def week_entries(request):
    entries = WeekEntry.objects.all().order_by('-week')  # Latest first
    return render(request, "forms/week_entries.html", {"entries": entries})

from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from datetime import timedelta
from .models import WeekEntry

def user_entries_list(request):
    """
    Display only the current user's submissions.
    Allow editing for 12 hours after submission.
    Most recent entries appear first.
    """
    user = request.user
    twelve_hours_ago = now() - timedelta(hours=12)

    # Get the user's own entries ordered by creation date (descending)
    entries = WeekEntry.objects.filter(submitted_by=user).order_by('-created_at')

    # Add an is_editable flag for each entry
    for entry in entries:
        entry.is_editable = entry.created_at >= twelve_hours_ago

    return render(request, "forms/user_entries.html", {"entries": entries})


from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import WeekEntryForm

@login_required
def edit_entry(request, entry_id):
    """
    Allow the user to edit their submission within 12 hours.
    """
    entry = get_object_or_404(WeekEntry, id=entry_id, submitted_by=request.user)
    twelve_hours_ago = now() - timedelta(hours=12)

    if entry.created_at < twelve_hours_ago:
        return HttpResponseForbidden("Editing time expired.")

    if request.method == "POST":
        form = WeekEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect("user_entries_list")
    else:
        form = WeekEntryForm(instance=entry)

    return render(request, "forms/edit_entry.html", {"form": form})

from django.http import JsonResponse
from .models import WeekEntry

def get_entry_data(request, entry_id):
    """
    Fetch entry data for editing via AJAX.
    """
    try:
        # Retrieve the entry
        entry = WeekEntry.objects.get(id=entry_id, submitted_by=request.user)

        # Return the data as JSON
        data = {
            'bay': entry.bay.name,  # Assuming there's a related model for Bay
            'bed_no': entry.bed_no.code,  # Assuming there's a related model for Bed
            'variety': entry.variety.name,  # Assuming there's a related model for Variety
            'amounts': entry.amounts,
            'date': entry.date.strftime('%Y-%m-%d'),  # Format date as needed
        }
        return JsonResponse(data)
    except WeekEntry.DoesNotExist:
        return JsonResponse({'error': 'Entry not found or not authorized to view this entry.'}, status=404)

from django.http import JsonResponse
from .models import Bay, Bed, Variety

def get_bed_and_bay_for_variety(request):
    variety_id = request.GET.get('variety_id')

    # Fetch bed and bay info based on variety_id
    if variety_id:
        variety = Variety.objects.get(id=variety_id)
        bed = variety.bed  # Assuming that a variety has a ForeignKey to Bed
        bay = bed.bay  # Assuming that a bed has a ForeignKey to Bay
        
        return JsonResponse({
            'bed_id': bed.id,
            'bed_code': bed.code,
            'bay_id': bay.id,
            'bay_name': bay.name
        })
    return JsonResponse({'error': 'Invalid variety ID'}, status=400)

from django.http import JsonResponse
from .models import Variety

def get_variety_suggestions(request):
    term = request.GET.get("term", "")
    varieties = Variety.objects.filter(name__icontains=term)[:10]
    suggestions = [{"label": v.name, "value": v.id} for v in varieties]
    return JsonResponse({"suggestions": suggestions})



from django.shortcuts import render
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
from .models import WeekEntry
import json

@login_required
def dynamic_dt_view(request):
    user = request.user  # Get current user

    # Aggregate data
    bay_data = WeekEntry.objects.values("bay__name").annotate(total_amounts=Sum("amounts"))
    bed_data = WeekEntry.objects.values("bed__code").annotate(total_amounts=Sum("amounts"))
    variety_data = WeekEntry.objects.values("variety__name").annotate(total_amounts=Sum("amounts"))

    # User-specific data
    user_data = WeekEntry.objects.filter(submitted_by=user).values("week").annotate(total_amounts=Sum("amounts"))

    # Weekly Trend (All Users)
    weekly_trend = WeekEntry.objects.values("week").annotate(total_amounts=Sum("amounts")).order_by("week")

    # Submission Activity Heatmap (Counts per Week)
    submission_activity = WeekEntry.objects.values("week").annotate(submissions=Count("id"))

    # Convert QuerySet to JSON
    bay_chart_data = [{"name": item["bay__name"], "data": [item["total_amounts"]]} for item in bay_data]
    bed_chart_data = [{"name": item["bed__code"], "data": [item["total_amounts"]]} for item in bed_data]
    variety_chart_data = [{"name": item["variety__name"], "data": [item["total_amounts"]]} for item in variety_data]
    weekly_chart_data = [{"week": item["week"], "amounts": item["total_amounts"]} for item in weekly_trend]
    submission_activity_data = [{"week": item["week"], "submissions": item["submissions"]} for item in submission_activity]
    user_chart_data = [{"week": item["week"], "amounts": item["total_amounts"]} for item in user_data]

    context = {
        "bay_chart_data": json.dumps(bay_chart_data),
        "bed_chart_data": json.dumps(bed_chart_data),
        "variety_chart_data": json.dumps(variety_chart_data),
        "weekly_chart_data": json.dumps(weekly_chart_data),
        "submission_activity_data": json.dumps(submission_activity_data),
        "user_chart_data": json.dumps(user_chart_data),
    }
    return render(request, "dyn_dt/index.html", context)


from django.shortcuts import get_object_or_404, render, redirect
from .models import WeekEntry

def edit_entry_modal(request, pk):
    entry = get_object_or_404(WeekEntry, pk=pk)

    if request.method == 'POST':
        entry.week = request.POST.get('week', entry.week)
        entry.bay_id = request.POST.get('bay', entry.bay.id)
        entry.bed_id = request.POST.get('bed', entry.bed.id)
        entry.variety_id = request.POST.get('variety', entry.variety.id)
        entry.amounts = request.POST.get('amounts', entry.amounts)
        entry.save()

        return redirect('week_entries')  

    return render(request, 'partials/edit_entry_form.html', {'entry': entry})

def edit_entry_modal(request, pk):
    entry = get_object_or_404(WeekEntry, pk=pk)

    if request.method == 'POST':
        entry.week = request.POST.get('week', entry.week)
        entry.bay_id = request.POST.get('bay', entry.bay.id)
        entry.bed_id = request.POST.get('bed', entry.bed.id)
        entry.variety_id = request.POST.get('variety', entry.variety.id)
        entry.amounts = request.POST.get('amounts', entry.amounts)
        entry.updated_by = request.user  # 👈 Track who made the update
        entry.save()
        return redirect('week_entries')  # or JsonResponse({'success': True})

    return render(request, 'partials/edit_entry_form.html', {'entry': entry})

# from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.models import User
# from .models import WeekEntry

# def user_entry_history(request, user_id):
#     user = get_object_or_404(User, pk=user_id)
#     entries = WeekEntry.objects.filter(submitted_by=user).order_by('-created_at')
#     return render(request, 'formflow/user_history.html', {
#         'user': user,
#         'entries': entries
#     })

# views.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

@staff_member_required
def staff_dashboard_view(request):
    return render(request, 'admin/staff_dashboard.html')


# views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from formflow.models import Variety

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from formflow.models import House, Bay, Bed, Variety
import openpyxl

@staff_member_required
def import_varieties_view(request):
    if request.method == "POST":
        excel_file = request.FILES.get("excel_file")
        try:
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active
            for row in sheet.iter_rows(min_row=2, values_only=True):
                house_name, bay_name, bed_code, variety_name = row
                if not all([house_name, bay_name, bed_code, variety_name]):
                    continue
                house, _ = House.objects.get_or_create(name=house_name)
                bay, _ = Bay.objects.get_or_create(name=bay_name, house=house)
                bed, _ = Bed.objects.get_or_create(code=bed_code, bay=bay)
                Variety.objects.create(name=variety_name, bed=bed)
            messages.success(request, "Varieties imported successfully.")
            return redirect("variety_list")
        except Exception as e:
            messages.error(request, f"Error reading Excel file: {e}")
    return render(request, "dashboard/import_varieties.html")

@staff_member_required
def variety_list_view(request):
    varieties = Variety.objects.select_related('bed__bay__house').all()
    return render(request, 'dashboard/variety_list.html', {'varieties': varieties})

@staff_member_required
def bed_list_view(request):
    beds = Bed.objects.select_related('bay__house').all()
    return render(request, 'dashboard/bed_list.html', {'beds': beds})

@staff_member_required
def bay_list_view(request):
    bays = Bay.objects.select_related('house').all()
    return render(request, 'dashboard/bay_list.html', {'bays': bays})

@staff_member_required
def house_list_view(request):
    houses = House.objects.all()
    return render(request, 'dashboard/house_list.html', {'houses': houses})

@staff_member_required
def user_list_view(request):
    users = User.objects.all()
    return render(request, 'dashboard/user_list.html', {'users': users})

@staff_member_required
def dashboard_view(request):
    return render(request, "admin/staff_dashboard.html")