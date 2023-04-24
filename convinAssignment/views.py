from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from django.views.generic import TemplateView



FLOW = Flow.from_client_config(
    client_config={
        "web": {
            "client_id": "75745113094-lb8q7urrc98llgqcedhj10bis5lldcmd.apps.googleusercontent.com",
            "client_secret": "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",
            "redirect_uris": ["http://localhost:8000/rest/v1/calendar/redirect/"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        }
    },
    scopes=["https://www.googleapis.com/auth/calendar"],
)

class HomeView(TemplateView):
    template_name = "home.html"

class GoogleCalendarInitView(View):
    def get(self, request):
        authorization_url, _ = FLOW.authorization_url(prompt="consent")
        return redirect(authorization_url)

class GoogleCalendarRedirectView(View):
    def get(self, request):
        code = request.GET.get("code")
        FLOW.fetch_token(code=code)
        credentials = FLOW.credentials

        service = build("calendar", "v3", credentials=credentials)
        events = service.events().list(calendarId="primary").execute()

        return JsonResponse(events)