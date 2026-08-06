from django import template

register = template.Library()


PLATFORM_ICONS = {
    "PC": {
        "icon": "windows",
        "class": "platform-windows"
    },
    "Windows": {
        "icon": "windows",
        "class": "platform-windows"
    },

    "PlayStation": {
        "icon": "playstation",
        "class": "platform-playstation"
    },
    "PlayStation 4": {
        "icon": "playstation",
        "class": "platform-playstation"
    },
    "PlayStation 5": {
        "icon": "playstation",
        "class": "platform-playstation"
    },

    "Xbox": {
        "icon": "xbox",
        "class": "platform-xbox"
    },
    "Xbox One": {
        "icon": "xbox",
        "class": "platform-xbox"
    },
    "Xbox Series X|S": {
        "icon": "xbox",
        "class": "platform-xbox"
    },

    "Nintendo Switch": {
        "icon": "nintendo-switch",
        "class": "platform-switch"
    },
    "Nintendo Switch 2": {
        "icon": "nintendo-switch",
        "class": "platform-switch"
    },

    "Steam": {
        "icon": "steam",
        "class": "platform-steam"
    },

    "Linux": {
        "icon": "linux",
        "class": "platform-linux"
    },

    "Android": {
        "icon": "android",
        "class": "platform-android"
    },

    "Apple": {
        "icon": "apple",
        "class": "platform-apple"
    },

    "iOS": {
        "icon": "apple",
        "class": "platform-apple"
    },
}


@register.filter
def platform_icons(value):
    """
    Convierte:

    'PC, PlayStation 5, Xbox Series X|S'

    en

    [
        {
            "name": "PC",
            "icon": "windows",
            "class": "platform-windows"
        },
        ...
    ]
    """

    if not value:
        return []

    platforms = []

    for platform in value.split(","):

        platform = platform.strip()

        data = PLATFORM_ICONS.get(platform)

        if not data:
            continue

        platforms.append({
            "name": platform,
            "icon": data["icon"],
            "class": data["class"],
        })

    return platforms


@register.filter
def multiplayer_label(value):
    return "Multiplayer" if value else "Single Player"


@register.filter
def game_status(game):

    completed_sections = 0

    if game.trailers.exists():
        completed_sections += 1

    if game.screenshots.exists():
        completed_sections += 1

    if game.achievements.exists():
        completed_sections += 1

    if game.soundtracks.exists():
        completed_sections += 1

    if game.guides.exists():
        completed_sections += 1

    if game.dlcs.exists():
        completed_sections += 1

    if game.patch_notes.exists():
        completed_sections += 1


    if completed_sections == 0:
        return "empty"

    elif completed_sections == 7:
        return "completed"

    return "progress"