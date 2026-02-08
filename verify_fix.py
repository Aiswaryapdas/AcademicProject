
import os
import django
import sys
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

# Add project root to path
sys.path.append('d:/AcademicProject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AcademicProject.settings')
django.setup()

from guest.views import login
from Admin.views import admin_dashboard
from Admin.models import Admin

def add_session_to_request(request):
    """Annotate a request object with a session."""
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()

print("--- Verifying Login Fix ---")

# 1. Simulate Login POST
factory = RequestFactory()
data = {'txt_email': 'admin@gmail.com', 'txt_pass': 'admin123'}
request = factory.post('/guest/login/', data)
add_session_to_request(request)

response = login(request)

print(f"Login Response Status Code: {response.status_code}")
if response.status_code == 302:
    print(f"Redirect URL: {response.url}")
    if response.url == '/WAdmin/admin_dashboard/': # internal Django redirect uses resolved URL or name, here likely simplified
        print("Redirect is correct.")
    
    # Check session
    print(f"Session Keys: {request.session.keys()}")
    if 'admin_id' in request.session:
        print("SUCCESS: 'admin_id' found in session.")
    else:
        print("FAILURE: 'admin_id' NOT found in session.")
else:
    print("FAILURE: Login did not redirect.")

print("\n--- Verifying Dashboard Fix ---")

# 2. Simulate Dashboard Access with Session
dashboard_request = factory.get('/WAdmin/admin_dashboard/')
add_session_to_request(dashboard_request)
dashboard_request.session['admin_id'] = 1 # Manually set valid session
dashboard_request.session.save()

try:
    dashboard_response = admin_dashboard(dashboard_request)
    print(f"Dashboard Response Status Code: {dashboard_response.status_code}")
    if dashboard_response.status_code == 200:
        print("SUCCESS: Dashboard loaded successfully (200 OK).")
        # Check content if possible (byte string)
        if b'faculty_count' in dashboard_response.content: # Context variables won't be in content unless rendered template uses them visible
             pass 
    else:
         print(f"FAILURE: Dashboard returned {dashboard_response.status_code}")
except Exception as e:
    print(f"FAILURE: Dashboard raised exception: {e}")
    import traceback
    traceback.print_exc()

