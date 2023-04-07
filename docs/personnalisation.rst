Personnalisation du site
=========================

Barre de navigation
*********************

Pour modifier le logo présent dans la barre de navigation du site, ouvrez le fichier ``/site_cuisineries/templates/site_cuisineries/navbar.html`` et modifiez l'url présente à la ligne suivante avec l'url de votre logo.

.. code-block:: html
    :caption: navbar.html
    :linenos:
    :lineno-start: 12
    :emphasize-lines: 2

        <a class="navbar-brand" href="/">
            <img src="/static/img/cropped-Logo-les-cuisineries.png" alt="Les cuisineries" height="24">
        </a>

Globale
*********

Dans le fichier ``/static/css/index.css``, vous pouvez modifier la partie suivante :

.. literalinclude:: ../static/css/index.css
    :language: css
    :caption: index.css
    :linenos:
    :lines: 1-8

Calendrier
************

Dans le fichier ``/static/css/calendar.css``, vous pouvez modifier la partie suivante :

.. literalinclude:: ../static/css/calendar.css
    :language: css
    :caption: calendar.css
    :linenos:
    :lines: 1-22

Panneau d'administration
**************************

Dans le fichier ``/static/css/admin.css``, vous pouvez modifier la partie suivante :

.. literalinclude:: ../static/css/admin.css
    :language: css
    :caption: admin.css
    :linenos:
    :lines: 1-43

Le logo présent dans la barre de navigation du panneau d'administration est modifiable dans le fichier ``/site_cuisineries/templates/admin/base_site.html``.

.. code-block:: html
    :caption: base_site.html
    :linenos:
    :lineno-start: 10

    <img src="{% static 'img/cropped-Logo-les-cuisineries.png' %}" alt="Les cuisineries" class="brand_img" height="50">