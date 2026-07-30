from django.shortcuts import render


# Create your views here.


def games_list(request):
    games = [

        {
            "id": 1,
            "title": "Cyberpunk 2077",
            "developer": "CD Projekt RED",
            "image": "assets/images/popular-01.jpg",
            "rating": 4.9,
            "genres": ["RPG", "Acción", "Mundo Abierto"],
            "platforms": [ 
                            {
                                "name": "PC",
                                "icon": "windows"
                            },
                            {
                                "name": "PlayStation",
                                "icon": "playstation"
                            },
                            {
                                "name": "Xbox",
                                "icon": "xbox"
                            }
            ],
            "players": "2.4 M",
            "release_year": 2020,
            "favorite": True,
        },
        {
            "id": 2,
            "title": "Halo Infinite",
            "developer": "343 Industries",
            "image": "assets/images/popular-02.jpg",
            "rating": 4.8,
            "genres": ["Shooter", "Acción", "Multijugador"],
            "platforms": [
                {"name": "PC", "icon": "windows"},
                {"name": "Xbox", "icon": "xbox"}
            ],
            "players": "1.8 M",
            "release_year": 2021,
            "favorite": False,
        },

        {
            "id": 3,
            "title": "Red Dead Redemption II",
            "developer": "Rockstar Games",
            "image": "assets/images/popular-03.jpg",
            "rating": 4.9,
            "genres": ["Aventura", "Acción", "Mundo Abierto"],
            "platforms": [
                {"name": "PC", "icon": "windows"},
                {"name": "PlayStation", "icon": "playstation"},
                {"name": "Xbox", "icon": "xbox"}
            ],
            "players": "5.2 M",
            "release_year": 2018,
            "favorite": True,
        },

        {
            "id": 4,
            "title": "Forza Horizon 5",
            "developer": "Playground Games",
            "image": "assets/images/popular-04.jpg",
            "rating": 4.7,
            "genres": ["Carreras", "Simulación", "Mundo Abierto"],
            "platforms": [
                {"name": "PC", "icon": "windows"},
                {"name": "Xbox", "icon": "xbox"}
            ],
            "players": "2.0 M",
            "release_year": 2021,
            "favorite": False,
        },

        {
            "id": 5,
            "title": "Elden Ring",
            "developer": "FromSoftware",
            "image": "assets/images/popular-05.jpg",
            "rating": 4.9,
            "genres": ["RPG", "Acción", "Soulslike"],
            "platforms": [
                {"name": "PC", "icon": "windows"},
                {"name": "PlayStation", "icon": "playstation"},
                {"name": "Xbox", "icon": "xbox"}
            ],
            "players": "3.6 M",
            "release_year": 2022,
            "favorite": True,
        },

        {
            "id": 6,
            "title": "God of War Ragnarök",
            "developer": "Santa Monica Studio",
            "image": "assets/images/popular-06.jpg",
            "rating": 4.9,
            "genres": ["Acción", "Aventura", "Hack & Slash"],
            "platforms": [
                {"name": "PlayStation", "icon": "playstation"}
            ],
            "players": "2.7 M",
            "release_year": 2022,
            "favorite": False,
        },

        {
            "id": 7,
            "title": "The Witcher 3",
            "developer": "CD Projekt RED",
            "image": "assets/images/popular-07.jpg",
            "rating": 4.8,
            "genres": ["RPG", "Aventura", "Mundo Abierto"],
            "platforms": [
                {"name": "PC", "icon": "windows"},
                {"name": "PlayStation", "icon": "playstation"},
                {"name": "Xbox", "icon": "xbox"},
                {"name": "Nintendo Switch", "icon": "nintendo-switch"}
            ],
            "players": "4.5 M",
            "release_year": 2015,
            "favorite": True,
        },

        {
            "id": 8,
            "title": "Assassin's Creed Shadows",
            "developer": "Ubisoft",
            "image": "assets/images/popular-08.jpg",
            "rating": 4.6,
            "genres": ["Acción", "RPG", "Sigilo"],
            "platforms": [
                {"name": "PC", "icon": "windows"},
                {"name": "PlayStation", "icon": "playstation"},
                {"name": "Xbox", "icon": "xbox"}
            ],
            "players": "1.5 M",
            "release_year": 2025,
            "favorite": False,
        },

        {
            "id": 9,
            "title": "Minecraft",
            "developer": "Mojang Studios",
            "image": "assets/images/popular-01.jpg",
            "rating": 4.8,
            "genres": ["Sandbox", "Supervivencia", "Aventura"],
            "platforms": [
                {"name": "PC", "icon": "windows"},
                {"name": "PlayStation", "icon": "playstation"},
                {"name": "Xbox", "icon": "xbox"}
            ],
            "players": "9.4 M",
            "release_year": 2011,
            "favorite": False,
        },

        {
            "id": 10,
            "title": "Resident Evil 4 Remake",
            "developer": "Capcom",
            "image": "assets/images/popular-02.jpg",
            "rating": 4.8,
            "genres": ["Terror", "Acción", "Supervivencia"],
            "platforms": [
                {"name": "PC", "icon": "windows"},
                {"name": "PlayStation", "icon": "playstation"},
                {"name": "Xbox", "icon": "xbox"}
            ],
            "players": "1.9 M",
            "release_year": 2023,
            "favorite": True,
        },

        {
            "id": 11,
            "title": "Baldur's Gate 3",
            "developer": "Larian Studios",
            "image": "assets/images/popular-03.jpg",
            "rating": 5.0,
            "genres": ["RPG", "Estrategia", "Fantasía"],
            "platforms": [
                {"name": "PC", "icon": "windows"},
                {"name": "PlayStation", "icon": "playstation"}
            ],
            "players": "2.8 M",
            "release_year": 2023,
            "favorite": True,
        },
    ]
    
    return render(request, "games/games.html", {
        'games': games
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
