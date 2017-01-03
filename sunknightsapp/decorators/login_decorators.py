from django.contrib.auth.decorators import user_passes_test, login_required

pointsmanagerrequired = user_passes_test(lambda u: u.is_points_manager,
                                   login_url='/')
warmanagerrequired = user_passes_test(lambda u: u.is_war_manager,
                                           login_url='/')

def points_manager_required(view_func):
    decorated_view_func = login_required(pointsmanagerrequired(view_func))
    return decorated_view_func

def war_manager_required(view_func):
    decorated_view_func = login_required(warmanagerrequired(view_func))
    return decorated_view_func