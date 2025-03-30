import hmac
import hashlib
import subprocess
import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Set up logging
logger = logging.getLogger(__name__)

@csrf_exempt
def update_from_github(request):
    # Log the request headers
    logger.info(f"Received webhook request with headers: {dict(request.headers)}")
    
    # Verify GitHub webhook signature
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        logger.error("No signature found in request")
        return HttpResponse('No signature', status=400)

    # Webhook secret - make sure this matches exactly what you set in GitHub
    secret = b'1ef159a174f3dc8b7f8297e357293fda6556da57c73d406bb200cdfbbbdb5f3b'
    
    # Calculate expected signature
    expected = 'sha256=' + hmac.new(
        secret,
        request.body,
        hashlib.sha256
    ).hexdigest()

    logger.info(f"Received signature: {signature}")
    logger.info(f"Expected signature: {expected}")

    if not hmac.compare_digest(signature, expected):
        logger.error("Invalid signature")
        return HttpResponse('Invalid signature', status=403)

    # Run update script
    try:
        result = subprocess.run(['/home/nevus/update_from_github.sh'], shell=True, capture_output=True, text=True)
        logger.info(f"Update script output: {result.stdout}")
        if result.stderr:
            logger.error(f"Update script errors: {result.stderr}")
        return HttpResponse('Updated successfully')
    except Exception as e:
        logger.error(f"Error running update script: {str(e)}")
        return HttpResponse(f'Error updating: {str(e)}', status=500) 