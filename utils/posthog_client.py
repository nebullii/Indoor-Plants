import posthog
from django.conf import settings

posthog.project_api_key = settings.POSTHOG_API_KEY
posthog.host = getattr(settings, 'POSTHOG_HOST', 'https://app.posthog.com')
