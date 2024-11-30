from django.http import HttpResponseBadRequest
import logging

class BlockMalformedRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Allow only valid HTTP methods
            if request.method not in ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD']:
                logging.warning(f"Invalid HTTP method detected: {request.method}")
                return HttpResponseBadRequest("Invalid HTTP method.")
            
            # Check if the request body is malformed
            if b'\x00' in request.body:
                logging.warning(f"Malformed request body: {request.body}")
                return HttpResponseBadRequest("Malformed request detected.")
        except Exception as e:
            logging.error(f"Error in middleware: {e}")
            return HttpResponseBadRequest("Malformed request detected.")
        
        return self.get_response(request)
