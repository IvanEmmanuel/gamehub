from django.templatetags.static import static


def user_profile(request):

    if request.user.is_authenticated and hasattr(request.user, 'userprofile'):

        profile = request.user.userprofile

        avatar = profile.avatar

        return {
            'profile_picture': (
                avatar.url
                if avatar
                else static('assets/images/default-game-cover.png')
            ),
            'profile_name': request.user.get_full_name(),
            'profile_username': request.user.username,
            'profile_gamer_tag': profile.gamer_tag,
        }

    return {
        'profile_picture': static('assets/images/default-game-cover.png'),
        'profile_name': '',
        'profile_username': '',
        'profile_gamer_tag': '',
    }