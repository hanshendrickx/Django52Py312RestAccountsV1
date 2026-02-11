from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PatientComplaint, AIPrompt, PromptTemplate
from .serializers import (
    PatientComplaintSerializer,
    AIPromptSerializer,
    PromptTemplateSerializer,
    GeneratePromptSerializer
)
from .services import PromptGenerator


class PatientComplaintViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing patient complaints (Signs & Current Complaints).
    """
    queryset = PatientComplaint.objects.all()
    serializer_class = PatientComplaintSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """Set the created_by field to the current user."""
        serializer.save(created_by=self.request.user)
    
    def get_queryset(self):
        """Filter complaints to show only those created by the current user."""
        return PatientComplaint.objects.filter(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def generate_prompt(self, request, pk=None):
        """
        Generate an AI prompt for this complaint.
        """
        complaint = self.get_object()
        serializer = GeneratePromptSerializer(data=request.data)
        
        if serializer.is_valid():
            prompt_type = serializer.validated_data.get('prompt_type', 'combined')
            
            try:
                ai_prompt = PromptGenerator.create_ai_prompt(
                    complaint_id=complaint.id,
                    prompt_type=prompt_type
                )
                
                return Response(
                    AIPromptSerializer(ai_prompt).data,
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AIPromptViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing AI prompts (read-only).
    Prompts are created via the PatientComplaint generate_prompt action.
    """
    queryset = AIPrompt.objects.all()
    serializer_class = AIPromptSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter prompts to show only those for complaints created by the current user."""
        return AIPrompt.objects.filter(complaint__created_by=self.request.user)


class PromptTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing prompt templates (read-only for now).
    """
    queryset = PromptTemplate.objects.filter(is_active=True)
    serializer_class = PromptTemplateSerializer
    permission_classes = [IsAuthenticated]
