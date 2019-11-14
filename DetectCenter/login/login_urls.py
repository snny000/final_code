# -*- coding: utf-8 -*-
from django.conf.urls import url
import views
urlpatterns = [

    # user
    url(r'^user_registration/?$', views.UserRegistration.as_view()),
    # url(r'^user_authenticate$', views.UserAuthenticate.as_view()),
    url(r'^change_password/?$', views.UserChangePassword.as_view()),
    url(r'^reset_user_password/?$', views.ResetUserPassword.as_view()),
    url(r'^user_expire/?$', views.PasswordExpire.as_view()),
    url(r'^user_login/?$', views.UserLogin.as_view()),
    url(r'^user_logout/?$', views.UserLogout.as_view()),
    url(r'^user_to_role/?$', views.UserToRole.as_view()),
    url(r'^user_remove_role/?$', views.UserRemoveRole.as_view()),
    url(r'^user_remove_all/?$', views.UserRemoveAll.as_view()),
    url(r'^user_query_all/?$', views.UserQueryAll.as_view()),
    url(r'^get_user_number/?$', views.GetUserNumber.as_view()),
    url(r'^delete_user/?$', views.DeleteUser.as_view()),
    url(r'^change_user_info/?$', views.ChangeUserInfo.as_view()),

    # role
    url(r'^role_create/?$', views.CreateRole.as_view()),
    url(r'^role_delete/?$', views.DeleteRole.as_view()),
    url(r'^role_to_user/?$', views.RoleToUser.as_view()),
    url(r'^role_remove_user/?$', views.RoleRemoveUser.as_view()),
    url(r'^role_remove_all_user/?$', views.RoleRemoveAllUser.as_view()),
    url(r'^role_query_all/?$', views.RoleQueryAll.as_view()),
    url(r'^get_role_number/?$', views.GetRoleNumber.as_view()),
    url(r'^change_role_info/?$', views.ChangeRoleInfo.as_view()),

    # permission
    url(r'^user_query_permission/?$', views.UserQueryPermission.as_view()),
    url(r'^role_query_permission/?$', views.RoleQueryPermission.as_view()),
    url(r'^role_add_permission/?$', views.RoleAddPermission.as_view()),
    url(r'^role_delete_permission/?$', views.RoleDeletePermission.as_view()),
    url(r'^role_delete_all_permission/?$', views.RoleDeleteAllPermission.as_view()),
    url(r'^query_all_permissions/?$', views.QueryAllPermissions.as_view()),
    url(r'^get_permission_number/?$', views.GetPermissionNumber.as_view()),




]
