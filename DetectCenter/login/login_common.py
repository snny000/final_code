# -*- encoding:utf-8 -*-



def trans_user_registration_info(request_data):
    """
    解析用户注册的信息。
    :param request:
    :return:
    """
    registration_info = {}
    # registration_info['username'] = 'admin'
    # registration_info['role_id'] = 1
    print request_data
    if 'username' in request_data:
        registration_info['username'] = request_data['username']
    if 'password' in request_data:
        registration_info['password'] = request_data['password']
    if 'email' in request_data:
        registration_info['email'] = request_data['email']
    if 'first_name' in request_data:
        registration_info['first_name'] = request_data['first_name']
    if 'last_name' in request_data:
        registration_info['last_name'] = request_data['last_name']
    if 'role_id' in request_data:
        registration_info['role_id'] = request_data['role_id']
    return registration_info


def trans_user_change_password(request_data):
    """
    解析修改密码
    :param request_data:
    :return:
    """
    user_info = {}
    # user_info['id'] = 2
    if 'id' in request_data:
        user_info['id'] = request_data['id']
    if 'username' in request_data:
        user_info['username'] = request_data['username']
    if 'old_password' in request_data:
        user_info['old_password'] = request_data['old_password']
    if 'new_password' in request_data:
        user_info['new_password'] = request_data['new_password']

    return user_info