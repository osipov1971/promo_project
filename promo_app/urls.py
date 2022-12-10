from django.urls import path, include

urlpatterns = [
    path('users/', include('promo_app.users.urls')),
#    path('mapping/', include('promo_app.assort_structure.mapping.urls')),
#    path('clustering/', include('promo_app.assort_structure.clustering.urls')),
#    path('assort_management/', include('promo_app.assort_management.urls')),
    path('common/', include('promo_app.common.urls')),
]