from calendar import c
from rest_framework.response import Response
from rest_framework import filters, generics, status
from rest_framework.views import APIView
from .serializers import PackageSerializer
from .models import Package


class PackageAPI(generics.ListCreateAPIView):
    serializer_class = PackageSerializer
    queryset = Package.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data 
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"status":"OK", "message":"Successfully created the package", "data":{"id": serializer.data['id']}},
                          status=status.HTTP_200_OK)
        
