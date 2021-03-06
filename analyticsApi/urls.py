from django.urls import path,re_path
from django.urls.resolvers import URLPattern
from rest_framework.generics import DestroyAPIView
from . import views


urlpatterns = [
path('api/user/register/', views.RegisterApiView.as_view(), name="register"),
path('api/admin/register/', views.AdminRegisterApiView.as_view(), name="admin-register"),
path('api/user/login/', views.LoginApiView.as_view(), name="user-login"),
path('api/admin/login/', views.LoginAdminApiView.as_view(),name="admin"),
path('api/user/current-user/', views.UserAPIView.as_view(), name="fetch-user"),
path('logout/', views.LogoutAPIView.as_view(), name="logout"),
path('api/activation-post/<int:phone_number>/', views.ActivationApiView.as_view(), name="ActivationPost"),
path('api/activate-user/<int:phone_number>/', views.ActivateUserApiView.as_view(), name="ActivatingUser"),
path('api/get-invalidcustomers/', views.GetAllUsers.as_view(), name="GetInvalidatedUsers"),
path('api/user/activation-documents/<int:phone_number>/', views.GetOneUserDocuments.as_view(), name="Getone_user_documents"),
path('api/user/notify_email/<int:phone_number>/', views.NotifyUserToUpload.as_view(), name="notify_email"),
path('api/user/notifyreupload_email/<int:phone_number>/', views.NotifyUserToReupload.as_view(), name="notify_email"),
path('api/get-account-details/<int:phone_number>/', views.GetUserAccountDetails.as_view(), name="get-account-details"),
path('api/create-new-account/<int:phone_number>/', views.CreateNewAccount.as_view(), name="create_account"),
path('api/maketransaction/<int:phone_number>/', views.MakeTransactions.as_view(), name="make-transaction"),
path('api/deposit/<int:phone_number>/', views.DepositApiView.as_view(), name="deposit"),
path('api/get/transactions/', views.getAllTransactionsApiView.as_view(), name="get_transaction"),
path('api/get/user-transactions/<int:phone_number>/', views.getUserTransactionApiView.as_view(), name='user_transactions'),
path('api/get/categories/', views.getAllCategoriesApiView.as_view(), name="categories"),
path('api/filter/category/<int:phone_number>/<int:category>/',views.getTransactioninCategoryApiView.as_view(),name="filter_by_category")
]
