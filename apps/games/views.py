from django.shortcuts import render
from .models.game import Game
from django.db.models import Q


# Create your views here.


def games_list(request):
    
    games = Game.objects.all()
    query = request.GET.get("q")
    
    if query:
        games = games.filter(
            Q(name__icontains= query) | Q(developer__icontains= query)
        )
    
    return render(request, "games/games.html", {
        'games': games,
        'query': query
    })


def games_detail(request):
    games = {

        "id": 1,

        "title": "Cyberpunk 2077",

        "developer": "CD Projekt RED",

        "publisher": "CD Projekt RED",

        "release_date": "10 Dic 2020",

        "rating": 4.5,
        
        "content_link": "games_content",

        "reviews": "12.4K",

        "description": (
            "Cyberpunk 2077 es un RPG de acción en mundo abierto ambientado "
            "en Night City, donde tus decisiones afectan la historia."
        ),

        "cover": "assets/images/popular-01.jpg",

        "banner": "assets/images/banner-1.jpg",

        "genres": [
            "RPG",
            "Acción",
            "Mundo Abierto",
            "MMO"
        ],

        "platforms": [
            "windows",
            "playstation",
            "xbox"
        ]

    }
    return render(request, "games/games_detail.html", {
        'games': games
    })


def games_content(request):
    
    content = {

                "id": 1,

                "title": "Cyberpunk 2077",

                "banner": "assets/images/banner-1.jpg",

                # ===============================
                # TRAILERS
                # ===============================

                "trailers": [

                        {
                            "title": "Official Launch Trailer",
                            "author": "CD Projekt RED",
                            "date": "10 Dic 2020",
                            "duration": "2:18",
                            "thumbnail": "assets/images/banner-1.jpg",
                            "video_url": "https://youtube.com/..."
                        },

                        {
                            "title": "Phantom Liberty Trailer",
                            "author": "CD Projekt RED",
                            "date": "11 Jun 2023",
                            "duration": "3:02",
                            "thumbnail": "assets/images/banner-2.jpg",
                            "video_url": "https://youtube.com/..."
                        }

                    ],

                    # ===============================
                    # GALERÍA
                    # ===============================

                    "gallery": [

                        "assets/images/game-01.jpg",
                        "assets/images/game-02.jpg",
                        "assets/images/game-03.jpg",
                        "assets/images/game-04.jpg"

                    ],

                    # ===============================
                    # DLC
                    # ===============================

                    "dlcs": [

                        {

                            "name": "Phantom Liberty",

                            "type": "Expansión",

                            "release_date": "26 Sep 2023",

                            "description": "Nueva historia ambientada en Dogtown.",

                            "price": 29.99,

                            "cover": "assets/images/popular-01.jpg",

                            "url": "https://www.youtube.com/"

                        }

                    ],

                    # ===============================
                    # GUÍAS
                    # ===============================

                    "guides": [

                        {

                            "title": "Guía para principiantes",

                            "author": "NightCity Guide",

                            "pdf": "#"

                        },

                        {

                            "title": "Todos los finales",

                            "author": "Lore Master",

                            "pdf": "#"

                        }

                    ],

                    # ===============================
                    # LOGROS
                    # ===============================

                    "achievements": {

                        "completed": 35,

                        "total": 57,

                        "list": [

                            {

                                "title": "The Fool",

                                "description": "Completa el prólogo.",

                                "image": "assets/images/details-01.jpg",

                                "percentage": "85%",

                                "unlocked": True

                            },

                            {

                                "title": "Legend of Night City",

                                "description": "Alcanza el nivel máximo.",

                                "image": "assets/images/details-02.jpg",

                                "percentage": "12%",

                                "unlocked": False

                            }

                        ]

                    },

                    # ===============================
                    # SOUNDTRACK
                    # ===============================

                    "soundtrack": [

                        {

                            "title": "Never Fade Away",

                            "artist": "SAMURAI",

                            "duration": "4:12",

                            "spotify": "https://spotify.com/"

                        },

                        {

                            "title": "The Rebel Path",

                            "artist": "P.T. Adamczyk",

                            "duration": "3:45",

                            "spotify": "https://spotify.com/"

                        }

                    ],

                    # ===============================
                    # ACTUALIZACIONES
                    # ===============================

                    "updates": [

                        {

                            "version": "Patch 2.3",

                            "date": "17 Jul 2025",

                            "description": "Mejoras de rendimiento y corrección de errores.",

                            "url": "https://store.epicgames.com/"

                        },

                        {

                            "version": "Patch 2.2",

                            "date": "15 May 2025",

                            "description": "Nuevas funciones para Photo Mode.",

                            "url": "https://store.epicgames.com/"

                        }

                    ]

                }
    
    return render(request, 'games/games_content.html', {
        'content': content
    })
