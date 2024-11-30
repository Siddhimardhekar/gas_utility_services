from django.test import TestCase
from .models import Customer, ServiceRequest

class CustomerModelTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone_number="1234567890"
        )

    def test_customer_creation(self):
        self.assertEqual(self.customer.first_name, "John")
        self.assertEqual(self.customer.last_name, "Doe")
        self.assertEqual(self.customer.email, "john@example.com")
        self.assertEqual(self.customer.phone_number, "1234567890")

class ServiceRequestModelTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John", last_name="Doe", email="john@example.com", phone_number="1234567890"
        )
        self.service_request = ServiceRequest.objects.create(
            customer=self.customer,
            service_type="repair",
            description="Fix the pipeline",
            status="Pending"
        )

    def test_service_request_creation(self):
        self.assertEqual(self.service_request.service_type, "repair")
        self.assertEqual(self.service_request.description, "Fix the pipeline")
        self.assertEqual(self.service_request.status, "Pending")
        self.assertEqual(self.service_request.customer.first_name, "John")

    def test_service_request_str(self):
        self.assertEqual(str(self.service_request), f"Request {self.service_request.id} - repair")
        
####
from django.urls import reverse
from django.test import Client, TestCase
from .models import Customer, ServiceRequest

class ServiceRequestViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone_number="1234567890"
        )
        self.service_request = ServiceRequest.objects.create(
            customer=self.customer,
            service_type="repair",
            description="Fix the pipeline",
            status="Pending"
        )
        self.url_submit = reverse('submit_request')
        self.url_track = reverse('track_request')

    def test_submit_request_view(self):
        # Test that the form submission works
        response = self.client.post(self.url_submit, {
            'service_type': 'repair',
            'description': 'Fix the pipeline',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful form submission

    def test_track_request_view(self):
        # Test the request tracking view
        response = self.client.get(self.url_track)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "repair")
