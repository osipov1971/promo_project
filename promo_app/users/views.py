from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from promo_project.settings import PSYORG_CONFIG
from promo_app.common.permissions import AccessLevelFivePermission, IsAuthenticated
from .serializers import *
import psycopg2


class RoleWithUserView(ListAPIView):
    permission_classes = [IsAuthenticated, AccessLevelFivePermission]
    queryset = Role.objects.filter(state=True).order_by('pk')
    serializer_class = RoleListSerializer


class RoleListView(ModelViewSet):
    permission_classes = [IsAuthenticated, AccessLevelFivePermission]
    queryset = Role.objects.filter(state=True).order_by('pk')

    def get_serializer_class(self):
        if self.action == 'list':
            return RoleShortInfoSerializer
        else:
            return RoleWithRightsSerializer

    def perform_create(self, serializer):
        serializer.save(user_created=self.request.user.username,
                        user_updated=self.request.user.username, )

    def perform_update(self, serializer):
        serializer.save(user_updated=self.request.user.username, )

    def destroy(self, request, *args, **kwargs):
        role = self.get_object()
        if role.users.filter(is_active=1, role=role).exclude(is_superuser=1).count() > 0:
            return Response({"info": "Вы не можете удалить роль. У данной роли есть пользователи"},
                            status=HTTP_400_BAD_REQUEST)
        role.state = 0
        role.save()
        return Response({"info": "Роль удалена"}, status=HTTP_200_OK)


class CreateRightRoleView(APIView):
    permission_classes = [IsAuthenticated, AccessLevelFivePermission]

    @swagger_auto_schema(request_body=RightSerializer(many=True), responses={200: RightSerializer(many=True)})
    def post(self, request):
        def get_list_created_rightrole(data, role_id, username):
            def apply(item):
                item = RightForRole.objects.create(
                    role_id=role_id,
                    right_id=item['right'],
                    level=item['level'],
                    user_created=username,
                    user_updated=username
                )
                item = RightSerializer(item)
                return item.data

            return list(map(apply, data))

        rights = get_list_created_rightrole(request.data, request.data[0]['role'], request.user.username)
        return Response(rights, status=HTTP_200_OK)


class UpdateRightRoleView(APIView):
    permission_classes = [IsAuthenticated, AccessLevelFivePermission]

    @swagger_auto_schema(request_body=RightSerializer(many=True), responses={200: RightSerializer(many=True)})
    def put(self, request, role_id):
        def get_list_updated_rightrole(data, queryset, username):
            def apply(item1, item2):
                item2.right_id = item1['right']
                item2.user_updated = username
                item2.save()
                item2 = RightSerializer(item2)
                return item2.data

            return list(map(apply, data, queryset))

        rights_queryset = RightForRole.objects.filter(role_id=role_id).order_by('level')
        rights = get_list_updated_rightrole(request.data, rights_queryset, request.user.username)
        return Response(rights, status=HTTP_200_OK)


class CreateUserView(ModelViewSet):
    """
    post: Create a new user. You MUST pass "password": "string"
    """
    permission_classes = [IsAuthenticated, AccessLevelFivePermission]
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save(password=self.request.data['password'], user_created=self.request.user.username,
                        user_updated=self.request.user.username, )


class UserDetailView(ModelViewSet):
    """
    get: Get the selected user.
    put: Update field values. You MUST pass "password": "string"
    delete: Set field is_active = 0. The selected user will not be able to log in
    """
    serializer_class = UserSerializer
    queryset = CustomUser.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated, AccessLevelFivePermission]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        else:
            return UserSerializer

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = 0
        user.save()
        return Response({"info": "Пользователь удален"}, status=HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(query_serializer=PasswordSerialiser(), responses={'204': 'Password changed'})
    def put(self, request):
        self.object = self.get_object()
        serializer = PasswordSerialiser(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"status": HTTP_204_NO_CONTENT}, status=HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CurrentUserDetailView(ModelViewSet):
    """
    get: Get the current user.
    put: Update field values. You MUST pass "password": "string"
    """
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CurrentUserSerializer
        else:
            return UserSerializer

    def get_object(self):
        return self.request.user


class RemoveSelectedUsers(APIView):
    permission_classes = [IsAuthenticated, AccessLevelFivePermission]

    def delete(self, request):
        """
        {
            "users": [1, 2, 3, 4, 5 ...]
        }
        """
        users = tuple(request.data.get('users'))
        connection = psycopg2.connect(PSYORG_CONFIG)
        cursor = connection.cursor()
        # noinspection SqlResolve
        cursor.execute(f'UPDATE am_app_customuser SET is_active=false WHERE id IN {users}')
        cursor.close()
        connection.close()
        return Response({"status": HTTP_204_NO_CONTENT})
