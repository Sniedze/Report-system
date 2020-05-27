from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from .models import Report, Operation, Risk
from .serializers import ReportSerializer, OperationSerializer, RiskSerializer
from accounts_app.serializers import ProfileSerializer
from .permissions import IsOwnerOrNoAccess


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UsersReportView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrNoAccess, ]
    authentication_classes = [TokenAuthentication, ]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        user = get_object_or_404(User, id=self.request.data.get('user'))
        developer = get_object_or_404(User, id=self.request.data.get('developer'))
        validator = get_object_or_404(User, id=self.request.data.get('validator'))
        owner = get_object_or_404(User, id=self.request.data.get('owner'))
        serializer.save(developer=developer, validator=validator, owner=owner, user=user)
        return Response({"user_id": user.id},
                        status=HTTP_200_OK)

    def get_queryset(self):
        queryset = Report.objects.filter(user=self.request.user)
        return queryset

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ReportDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrNoAccess, ]
    authentication_classes = [TokenAuthentication, ]


class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer


class RisksViewSet(viewsets.ModelViewSet):
    queryset = Risk.objects.all()
    serializer_class = RiskSerializer


@login_required
def index(request):
    user = request.user
    user_profile = get_object_or_404(ProfileSerializer, user=user)
    role = user_profile.role
    reports = ReportSerializer.objects.all()
    if role == "developer":
        create_link = 'report_app:index'
        link_name = "Create Report"
    else:
        create_link = ""
        link_name = ""
    context = {
        'reports': reports,
        'create_link': create_link,
        'link_name': link_name

    }
    return render(request, 'report_app/index.html', context)


@login_required()
def create(request):
    pass
