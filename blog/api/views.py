from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import BlogListSerializer, UserSerializer
from ..models import Blog


class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'status': 403, 'errors': serializer.errors, "message": "Something went wrong!"})

        serializer.save()

        user = User.objects.get(username=serializer.data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({'status': 200, 'refresh': str(refresh), 'access': str(refresh.access_token),
                         "message": "posted successfully"})


class PostAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Blog.objects.all()
        serializer = BlogListSerializer(posts, many=True)
        return Response({'status': 200, 'payload': serializer.data})

    def post(self, request):
        serializer = BlogListSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": 403, "errors": serializer.errors, "message": "Something went wrong!"})
        serializer.save()
        return Response({'status': 200, 'message': 'posted successfully'})

    def put(self, request):
        pass

    def patch(self, request):
        try:
            post_obj = Blog.objects.get(id=request.data['id'])
            serializer = BlogListSerializer(post_obj, data=request.data, partial=True)

            if not serializer.is_valid():
                return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})
            serializer.save()

            return Response({"status": 200, "payload ": serializer.data, "msg": "patched successfully"})
        except Exception as e:  # noqa F841
            return Response({"status": 403, 'msg': "invalid id"})

    def delete(self, request):
        pass
