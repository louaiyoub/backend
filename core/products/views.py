from urllib import request

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.middleware.csrf import get_token
from .permission import IsEditor


#class ProductViewSet(ModelViewSet):
 #   queryset = Product.objects.all()
  #  serializer_class = ProductSerializer
  #  permission_classes = [IsAuthenticatedOrReadOnly]

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user:
            login(request, user)
            return HttpResponse("Logged in ")
        else:
            return HttpResponse("Invalid credentials ")

    csrf_token = get_token(request)

    return HttpResponse(f"""
        <html>
            <body>
                <h2>Login</h2>
                <form method="post">
                    <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                    <input type="text" name="username" placeholder="Username"><br><br>
                    <input type="password" name="password" placeholder="Password"><br><br>                    
                    <button type="submit">Login</button>
                </form>
            </body>
        </html>
    """)
@api_view(['GET'])


def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# CREATE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# UPDATE
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    

    return Response(serializer.errors, status=400)
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_product(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

    product.delete()
    return Response(status=204)
@api_view(['GET','PUT'])
@permission_classes([IsEditor])
def get_or_update_product(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

    if request.method == 'GET':
        serializer = ProductSerializer(product,context={'request': request})
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
