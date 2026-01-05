from django.urls import path
from .views import HelpCenterView, HelpReportView, HelpCenterDetail, HelpCenterAnswers
app_name = 'help'

urlpatterns = [
    path('', HelpCenterView.as_view(), name='help-center'),
    path('<int:id>/', HelpCenterDetail.as_view(), name='help-detail'),
    path('detail/<int:id>', HelpCenterAnswers.as_view(), name='help-answer-detail'),
    path('reports/', HelpReportView.as_view(), name='help_reports'),

]