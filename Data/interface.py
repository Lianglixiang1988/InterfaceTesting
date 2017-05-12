config = {
    'setting': {
        'method_name': 'runTest',
        'environment': 'dev',
        'port': 7070
    },
    'dev': {
        'base_url': 'http://10.0.10.87',
        'db_host': '10.0.10.87',
        'db_port': 3306,
        'db_schema': 'vrserver',
    },
    'api': {
        'account': {
            'login': '/rest/api/account/login',
            'logout': '/rest/api/account/logout ',
            'send_sms': '/rest/api/account/sendsms',
            'valid_mobile': '/rest/api/account/validmobile',
            'mobile_used': '/rest/api/account/mobileused',
            'register': '/rest/api/account/register',
            'modify_profile': '/rest/api/account/register',
            'query_profile': '/rest/api/account/queryprofile',
            'reset_password': '/rest/api/account/resetpassword',
            'valid_nickname': '/rest/api/account/validnickname',
            'v_code': '/rest/api/account/vcode',
            'query_user_role': '/rest/api/account/role?token=',
        },
        'health': '/rest',
        'oauth': '/rest/api/oauth/token?access_token=',
        'room': {
            'create_room': '/rest/api/rooms?access_token=',
            'update_room': '/rest/api/rooms/',
            'query_room': '/rest/api/rooms/',
            'add_room_user': '/rest/api/room_users?access_token=',
            'delete_room_user': '/rest/api/room_users?access_token=',
            'delete_room': '/rest/api/rooms/',
        },
        'session': {
            'create_session': '/rest/api/sessions',
            'delete_session': '/rest/api/sessions?token=',
            'update_session': '/rest/api/sessions',
            'query_session': '/rest/api/sessions',
            'add_session_user': '/rest/api/session_users',
            'query_session_user': '/rest/api/session_users?token=',
            'delete_session_user': '/rest/api/session_users?token=',
        },
        'firmware': {
            'get_firmware': '/rest/api/firmware/latestversion?type=client&pid=pid&secret=N3Ld6PpBKd0vwUtywQ63',
            'create_firmware': '/rest/api/firmware/latestversion'
        },
        'big_data': {
            'register': '/rest/api/collector/register',
            'upload': '/rest/api/collector/data'
        },
        'shop': {
            'refresh': '/rest/api/hshop/cartitem',
            'delete': '/rest/api/hshop/cartitem?token=',
            'query': '/rest/api/hshop/cartitem?token=',
            'order': '/rest/api/hshop/order',
            'update_order': '/rest/api/hshop/order',
            'query_order': '/rest/api/hshop/order?token=',
            'query_order_detail': '/rest/api/hshop/orderdetail?order_no=',
            'payment': '/rest/api/ali/payment',
            'query_payment': '/rest/api/ali/payment?token=',
            'refunds': '/rest/api/ali/refund_apply',
        },
        'p2p': {
            'create': '/rest/api/im/im_acc',
            'refresh': '/rest/api/im/refresh_im_token',
            'query': '/rest/api/im/im_acc?token=',
            'send_msg': '/rest/api/im/batch_msg',
        },
        'Membership': {
            'create_Membership_order': '/rest/api/membership/order',
            'check_user_info': '/rest/api/membership/user-info',
            'check_Membership_list': '/rest/api/membership/sellableItems',
        },
        'GameOrder': {
            'check_user_all_game': '/rest/api/game/ordered',
            'create_game_order': '/rest/api/game/order',
            'check_game_status': '/rest/api/game/order/',
        },
        'developer_dev': {
            'developer_dev': '/rest/api/developer/apply-dev',
        }
    }
}
