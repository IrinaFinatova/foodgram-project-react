from .views import RecipeViewSet, TagViewSet, IngredientViewSet, FavoriteViewSet, CartViewSet
from rest_framework.routers import DefaultRouter
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r"ingredients", IngredientViewSet, basename="ingredients")
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"recipes", RecipeViewSet, basename="recipes")
router.register(
    r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteViewSet, basename='favorites')
router.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart', CartViewSet, basename='cart')
#router.register(r"tags", TagViewSet, basename="tags")
#router.register(
#    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
#)
##router.register(
#    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
#    CommentViewSet,
#    basename="comments",
#)


#token = [
 #   path("signup/", CreateUserAPIView.as_view(), name="signup"),
#    path("token/", GetTokenAPIView.as_view(), name="token"),
#]


urlpatterns = [
    path('', include(router.urls)),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)