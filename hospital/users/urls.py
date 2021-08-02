from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import HospitalUserCreateView, HospitalUserUpdateView, \
    HospitalUserBlockingView, DoctorFreeSlotGetterView, \
    AppointmentWithDoctor, AllEntries, UndoAppointmentWithDoctor

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user/create', HospitalUserCreateView.as_view(), name='users-create'),
    path('user/update/<int:pk>', HospitalUserUpdateView.as_view(),
         name='users-update'),
    path('user/blocking/<int:pk>', HospitalUserBlockingView.as_view(),
         name='users-blocking'),

    path('doctor/slots/get/<int:pk>', DoctorFreeSlotGetterView.as_view(),
         name='get-slots'),
    path('doctor/appointment/<int:pk>', AppointmentWithDoctor.as_view(),
         name='doctor-appointment'),
    path('doctor/appointment/undo/<int:pk>',
         UndoAppointmentWithDoctor.as_view(),
         name='undo-doctor-appointment'),
    path('doctor/entries/all', AllEntries.as_view(), name='users-update'),
]
