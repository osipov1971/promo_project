from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from promo_app.common.serializers import LanguageSerializer
from promo_app.models import Language, Category
from .permissions import *
from .serializers import CategoryListWithActiveBundleSerializer


class LanguageListView(ReadOnlyModelViewSet):
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()


class CategoryWithActiveBundleView(ListAPIView):
    permission_classes = [IsAuthenticated, AccessLevelTwoPermission]
    serializer_class = CategoryListWithActiveBundleSerializer

    def get_queryset(self):
        return Category.objects.filter(
            categorydictionary__language__pk=self.request.user.language.pk,
            categorygroupproductlink__state=True
        ).exclude(state=False).distinct()
