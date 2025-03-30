import hmac
import hashlib
import subprocess
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

@csrf_exempt
def update_from_github(request):
    # Verify GitHub webhook signature
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        return HttpResponse('No signature', status=400)

    # Replace this with the same secret you used in GitHub webhook settings
    secret = b'your_secure_secret_here_123xyz'
    
    # Calculate expected signature
    expected = 'sha256=' + hmac.new(
        secret,
        request.body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected):
        return HttpResponse('Invalid signature', status=403)

    # Run update script
    subprocess.run(['/home/nevus/update_from_github.sh'], shell=True)
    return HttpResponse('Updated successfully') 