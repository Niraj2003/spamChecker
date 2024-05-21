from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import login
from api.authentication import PhoneNumberBackend
from .models import Contact
from .serializers import UserSerializer, ContactSerializer
from rest_framework.decorators import api_view

User = get_user_model()

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        name = self.request.data.get('name')
        phone_number = self.request.data.get('phone_number')
        password = self.request.data.get('password')
        
        user = serializer.save(password=make_password(password))

        contact_data = {'name': name, 'phone_number': phone_number}
        contact_serializer = ContactSerializer(data=contact_data)
        if contact_serializer.is_valid():
            contact_serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserLogin(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        user = PhoneNumberBackend().authenticate(request, phone_number=phone_number, password=password)
        print(user)
        if user is not None:
            login(request, user, backend='api.authentication.PhoneNumberBackend')
            return Response(UserSerializer(user).data)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def mark_spam(request):
    if request.user.is_authenticated != True: 
        return Response({'error': 'You must be logged in to mark spam contacts'}, status=status.HTTP_401_UNAUTHORIZED)

    phone_number = request.data.get('phone_number')
    
    if not phone_number:
        return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        contact = Contact.objects.get(phone_number=phone_number)
    except Contact.DoesNotExist:
        contact = Contact.objects.create(phone_number=phone_number)
    
    contact.spam_count += 1
    contact.save()
    
    contact_serializer = ContactSerializer(contact)
    
    return Response(contact_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def search(request):
    if request.user.is_authenticated != True: 
        return Response({'error': 'You must be logged in to mark spam contacts'}, status=status.HTTP_401_UNAUTHORIZED)

    query = request.query_params.get('query')
    search_type = request.query_params.get('type')

    if search_type == 'name':
        results_start_with = Contact.objects.filter(name__istartswith=query)
        results_contain = Contact.objects.filter(name__icontains=query).exclude(name__istartswith=query)
        results = list(results_start_with) + list(results_contain)
        
        results_data = []
        for contact in results:
            contact_data = ContactSerializer(contact).data
            contact_data['spam_likelihood'] = calculate_spam_likelihood(contact.phone_number)
            results_data.append(contact_data)

    elif search_type == 'phone_number':
        results_start_with = Contact.objects.filter(phone_number__istartswith=query)
        results = list(results_start_with)

        results_data = []
        for result in results:
            if isinstance(result, User):
                result_data = UserSerializer(result).data
            else:
                result_data = ContactSerializer(result).data
            result_data['spam_likelihood'] = calculate_spam_likelihood(result.phone_number)
            results_data.append(result_data)

    else:
        results_data = []
        results = list(User.objects.all()) + list(Contact.objects.all())

        for result in results:
            if isinstance(result, User):
                result_data = UserSerializer(result).data
            else:
                result_data = ContactSerializer(result).data
            result_data['spam_likelihood'] = calculate_spam_likelihood(result.phone_number)
            results_data.append(result_data)

    return Response(results_data, status=status.HTTP_200_OK)

def calculate_spam_likelihood(phone_number):
    x = Contact.objects.count()
    y = Contact.objects.get(phone_number=phone_number).spam_count
    return round(y / x * 100, 2)