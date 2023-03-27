Personnalisation du site
=========================

Calendrier
************

Dans le fichier ``/static/css/calendar.css``, vous pouvez modifier la partie suivante :

.. code-block:: css
    :caption: calendar.css
    :linenos:

    :root{
        /* Couleur de fond du header */
        --header-bg:#943c24;

        /* Couleur du texte du calendrier sur fond clair */
        --calendar-txt-color: var(--header-bg);

        /* Couleur du texte du calendrier sur fond sombre */
        --calendar-txt-color-dark: white;

        /* Contour et ombres du calendrier */
        --calendar-shadow: #c9c9c9;

        /* Couleur des vacations */
        --vacation-color: #f7b057;

        /* Couleur des réunions */
        --reunion-color: #e87333;

        /* Couleur du jour */
        --today-color: #e66b6b;
    }


Panneau d'administration
**************************

Dans le fichier ``/static/css/admin.css``, vous pouvez modifier la partie suivante :

.. code-block:: css
    :caption: admin.css
    :linenos:

    :root{
        /* Couleur de fond de la barre de navigation */
        --background-header-color: rgba(33,37,41,1);

        /* Couleur de fond du panneau d'administration */
        --background-color:#E7DBCB;

        /* Couleur du texte sur fond combre */
        --txt-color: white;

        /* Couleur du texte sur fond clair */
        --link-fg:black;

        /* Couleur des bandeaux principaux et des boutons */
        --primary: #943c24;

        /* Couleur principale des tableaux */
        --body-bg:#c99a8d;

        /* Couleur secondaire des tableaux */
        --darkened-bg:#bb8170;

        /* Couleur du texte des breadcrumbs */
        --breadcrumbs-fg:#c99a8d;

        /* Couleur de la ligne sélectionnée */
        --selected-row:#835a4e;

        /* Couleur de survol des textes du tableau */
        --object-tools-bg: var(--primary);
        --link-hover-color:var(--primary);
        --link-selected-fg:var(--primary);

        --object-tools-hover-bg: var(--darkened-bg);
        --hairline-color: transparent;
        --body-fg:black;
        --body-quiet-color:black;

        /* Images de fond du panneau d'administration*/
        --bg-left: url(/static/img/Ronds_petits.png);
        --bg-right: url(/static/img/Ronds_moyens.png);
    }