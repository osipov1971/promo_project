from rest_framework.permissions import BasePermission
from rest_framework.views import View
from rest_framework.request import Request
from promo_app.models import RightForRole


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class AccessPermission(BasePermission):
    level = 0

    def has_permission(self, request: Request, view: View):
        user_right: RightForRole = request.user.role.rightforrole_set.get(level=self.level).right.pk
        if request.method == 'GET':
            if (user_right == 3) or (user_right == 2):
                return True
        elif request.method in ['POST', 'PUT', 'PATCH', 'DELETE'] and (user_right == 3):
            return True
        return False


class AccessLevelOnePermission(AccessPermission):
    level = 1


class AccessLevelTwoPermission(AccessPermission):
    level = 2


class AccessLevelThreePermission(AccessPermission):
    level = 3


class AccessLevelFourPermission(AccessPermission):
    level = 4


class AccessLevelFivePermission(AccessPermission):
    level = 5


class AccessLevelSixPermission(AccessPermission):
    level = 6
