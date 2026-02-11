from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientComplaintViewSet, AIPromptViewSet, PromptTemplateViewSet

router = DefaultRouter()
router.register(r'complaints', PatientComplaintViewSet, basename='complaint')
router.register(r'prompts', AIPromptViewSet, basename='aiprompt')
router.register(r'templates', PromptTemplateViewSet, basename='template')

urlpatterns = [
    path('', include(router.urls)),
]
