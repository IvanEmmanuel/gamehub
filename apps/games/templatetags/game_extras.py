from django import template

register = template.Library()


PLATFORM_ICONS = {
    "PC": "windows",
    "Windows": "windows",
    "PlayStation": "playstation",
    "PlayStation 4": "playstation",
    "PlayStation 5": "playstation",
    "Xbox": "xbox",
    "Xbox One": "xbox",
    "Xbox Series X|S": "xbox",
    "Nintendo Switch": "nintendo-switch",
    "Nintendo Switch 2": "nintendo-switch",
    "Steam": "steam",
    "Linux": "linux",
    "Android": "android",
    "Apple": "apple",
    "iOS": "apple"
}


@register.filter
def platform_icons(value):
    """
    Convierte:
    'PC, PlayStation 5, Xbox Series X|S'

    en

    [
        ('PC', 'windows'),
        ('PlayStation 5', 'playstation'),
        ('Xbox Series X|S', 'xbox')
    ]
    """

    if not value:
        return []

    platforms = []

    for platform in value.split(","):
        platform = platform.strip()

        platforms.append({
            "name": platform,
            "icon": PLATFORM_ICONS.get(platform)
        })

    return platforms

@register.filter
def multiplayer_label(value):
    return "Multiplayer" if value else "Single Player"