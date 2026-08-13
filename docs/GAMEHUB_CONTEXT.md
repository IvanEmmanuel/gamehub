# GameHub — Contexto Maestro del Proyecto

> Documento de continuidad para retomar el desarrollo de GameHub en un chat nuevo.
> La fuente de verdad del código es el repositorio/proyecto actual. Este documento conserva además decisiones, objetivos y contexto que no necesariamente están explícitos en el código.

## 1. Proyecto

**GameHub** es una plataforma web de videojuegos desarrollada con Django.

El proyecto se basa en un curso de Django de DevTalles, pero se está adaptando una plataforma educativa a una plataforma de videojuegos.

Repositorio de GameHub:
- https://github.com/IvanEmmanuel/gamehub

Repositorio de referencia del profesor:
- https://github.com/DevTalles-corp/devilearn-django-project/tree/devilearn-version4-cbv-forms-auth-final

## 2. Principio de adaptación del curso

La regla general es **adaptar conceptos del curso, no copiar literalmente su dominio**.

- Instructor → Moderador de GameHub.
- Course → Game.
- Student → Usuario/Jugador.
- Enrollment → UserGameLibrary.
- Progress → posteriormente se estudiará como base conceptual para el sistema de logros del usuario.

No crear anticipadamente modelos o funcionalidades que todavía no sean necesarios.

## 3. Arquitectura conceptual

GameHub tiene tres áreas principales:

### Public
Experiencia de usuarios/jugadores:
- listado de juegos;
- detalle de juego;
- exploración del contenido;
- posteriormente biblioteca, perfil, reseñas, etc.

### Moderation
Área asociada al moderador y al flujo del curso correspondiente al instructor.

### Management
Administración del contenido asociado a cada juego.

Las URLs y vistas se separan por responsabilidad:

```text
apps/games/
├── models/
├── views/
│   ├── public.py
│   ├── moderation.py
│   └── management.py
├── urls/
│   ├── public.py
│   ├── moderation.py
│   └── management.py
└── urls.py
```

## 4. Namespaces de URLs

Las URLs públicas utilizan:

```python
app_name = "public"
```

Por ello, los templates deben usar:

```django
{% url 'public:games_list' %}
{% url 'public:games_detail' game.slug %}
{% url 'public:games_content' game.slug %}
```

No volver a utilizar nombres globales como `games_list` si la URL está namespaced.

La misma lógica se aplica a `moderation` y `management` cuando corresponda.

## 5. Modelos actuales de Games

Actualmente existen modelos para:

- Game
- Genre
- Achievement
- DLC
- Guide
- PatchNote
- Screenshot
- Soundtrack
- Trailer

Todavía NO deben asumirse como existentes:

- Review
- UserGameLibrary
- UserAchievement

Se implementarán cuando corresponda.

## 6. Estado de Management

La parte de Management para administrar contenido de juegos está terminada y probada.

Se implementó CRUD para:

- Trailers
- Screenshots
- Achievements
- Soundtrack
- DLC
- Guides
- Patch Notes

Según corresponda se implementaron:
- listado;
- crear;
- editar;
- eliminar;
- modales;
- Drag & Drop;
- persistencia del orden;
- JavaScript;
- CSS;
- URLs;
- vistas.

Patch Notes quedó probado con crear, editar, eliminar, Drag & Drop y persistencia de `display_order`.

No reconstruir estos módulos salvo que una nueva funcionalidad necesite integrarlos.

## 7. Área pública actual

Flujo:

```text
/games/
    ↓
Listado de juegos

/games/detail/<slug>/
    ↓
Detalle del juego

/games/<slug>/content/
    ↓
Explorar contenido
```

### Detalle de juego

Contempla:
- Hero;
- descripción;
- capturas;
- características;
- reseñas;
- noticias;
- ficha técnica;
- perfil del juego;
- juegos recomendados;
- requisitos del sistema;
- reseñas de la comunidad.

Parte de esta página todavía contiene información estática y se irá haciendo dinámica conforme avance el curso.

### Explorar contenido

Contempla:
- Trailers y videos;
- Capturas de pantalla;
- DLC y expansiones;
- Guías destacadas;
- Logros;
- Banda sonora;
- Actualizaciones / Patch Notes.

Los contenidos administrativos deben alimentar posteriormente esta experiencia pública.

## 8. Próxima funcionalidad: biblioteca

La próxima funcionalidad importante es la **biblioteca de juegos del usuario**.

La equivalencia con el curso es:

```text
Enrollment → UserGameLibrary
Course     → Game
Student    → User/Player
```

`UserGameLibrary` representará:

> Este juego pertenece a la biblioteca de este usuario.

Conceptualmente:

```text
User
  │
  └── UserGameLibrary
          │
          └── Game
```

Debe impedirse que el mismo usuario agregue el mismo juego múltiples veces.

## 9. Flujo esperado de biblioteca

En el Hero del detalle del juego existe:

```text
♡ Agregar a mi biblioteca
```

Al pulsarlo:

```text
Game Detail
    ↓
Agregar a mi biblioteca
    ↓
crear UserGameLibrary
    ↓
guardar
    ↓
redirigir a Mi Biblioteca
```

Ejemplo:

```text
Halo Infinite
    ↓
♡ Agregar a mi biblioteca
    ↓
UserGameLibrary creada
    ↓
Mi Biblioteca
    ↓
Halo Infinite aparece
```

La redirección inmediata a la biblioteca es intencional.

## 10. Estado del corazón y botón

Si el juego NO pertenece a la biblioteca:

```text
♡ Agregar a mi biblioteca
```

Si YA pertenece:

```text
♥ En mi biblioteca
```

con posibilidad de:

```text
Quitar de mi biblioteca
```

Cuando el usuario vuelva posteriormente al detalle del juego, el corazón debe aparecer marcado si existe la relación.

Inicialmente se puede implementar con POST + redirect. No introducir AJAX todavía.

Flujo completo:

```text
Games
  ↓
Halo Infinite
  ↓
♡ Agregar a mi biblioteca
  ↓
UserGameLibrary
  ↓
Mi Biblioteca
  ↓
Halo Infinite aparece
  ↓
Volver a Games
  ↓
♥ En mi biblioteca
  ↓
Quitar de mi biblioteca
  ↓
♡ Agregar a mi biblioteca
```

## 11. Progress y logros

NO utilizar Progress para:
- ver trailers;
- leer guías;
- escuchar soundtrack;
- marcar contenido multimedia como visto.

Eso no encaja con la experiencia de GameHub.

El concepto de `Progress` se estudiará posteriormente para los **logros del usuario**.

Idea futura:

```text
UserAchievement
    user
    achievement
    completed
    completed_at
```

Ejemplo:

```text
Halo Infinite

Logros
37 / 50

██████████████░░░░░░ 74%

☑ Achievement A
☑ Achievement B
☐ Achievement C
☐ Achievement D
```

El porcentaje puede calcularse como:

```text
logros completados / logros totales
```

No implementar `UserAchievement` todavía. Primero terminar `UserGameLibrary` y analizar el `Progress` real del profesor.

## 12. Orden de trabajo

### Fase actual
Analizar la implementación real de `Enrollment` del profesor:
- modelo;
- relaciones;
- vistas;
- forms;
- URLs;
- templates;
- uso de `request.user`;
- creación;
- eliminación;
- protección contra duplicados;
- redirección.

### Siguiente
Adaptar:

```text
Enrollment → UserGameLibrary
```

### Después
Conectar:

```text
♡ Agregar a mi biblioteca
```

### Después
Crear/terminar:

```text
Mi Biblioteca
```

### Después
Estado dinámico:

```text
♡ / ♥
Agregar / En biblioteca
```

### Después
Eliminar de biblioteca.

### Después
Analizar `Progress` y decidir la adaptación para logros.

## 13. Decisiones de UX

- Agregar un juego debe llevar al usuario directamente a su biblioteca.
- Volver al detalle debe reflejar el estado actual de la biblioteca.
- El corazón representa si el juego pertenece a la biblioteca.
- No convertir cada pieza de contenido en una unidad de progreso.
- Los logros son el candidato natural para el progreso futuro.

## 14. Funcionalidades futuras

Pendientes, entre otras:
- Biblioteca de juegos;
- Logros del usuario;
- Reseñas;
- estadísticas;
- perfil;
- recomendaciones dinámicas;
- noticias;
- requisitos del sistema dinámicos;
- funcionalidades que el curso vaya introduciendo.

Seguir el orden pedagógico del curso y adaptar cada concepto a GameHub.

## 15. Reglas para continuar

1. Revisar primero el código actual antes de asumir nombres o estructuras.
2. Usar el proyecto local/repositorio como fuente de verdad del código.
3. Usar este documento como fuente de decisiones y contexto.
4. No inventar modelos que todavía no existen.
5. No modificar módulos terminados sin una razón concreta.
6. Adaptar los patrones técnicos del profesor al dominio de videojuegos.
7. Implementar una etapa a la vez.
8. Probar cada etapa antes de avanzar.
9. Explicar brevemente qué se adapta y por qué.
10. No adelantarse a Progress/UserAchievement mientras UserGameLibrary no esté terminado.

## 16. Próximo objetivo exacto

> Analizar la implementación real de `Enrollment` en el proyecto del profesor y adaptarla a `UserGameLibrary` en GameHub.

Antes de escribir código:
- identificar cómo funciona `Enrollment`;
- explicar la equivalencia;
- indicar qué archivos se modificarán/crearán;
- implementar paso a paso;
- probar cada parte.

## 17. Curso de referencia

Proyecto del profesor:

https://github.com/DevTalles-corp/devilearn-django-project/tree/devilearn-version4-cbv-forms-auth-final

El curso es una guía técnica. GameHub debe conservar su propia identidad y dominio.

## 18. Meta del proyecto

GameHub debe terminar como una plataforma de videojuegos coherente y útil como proyecto de portafolio, con:
- buenas relaciones entre modelos;
- autenticación;
- CBVs/forms cuando correspondan;
- separación clara de responsabilidades;
- funcionalidades reales de usuario;
- código mantenible;
- arquitectura consistente.
