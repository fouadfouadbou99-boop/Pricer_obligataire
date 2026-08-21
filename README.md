# Pricer Obligataire Maroc

Cette application Streamlit permet de pricer des obligations et de calculer leur duration de Macaulay en utilisant une courbe de taux zéro.

## Structure du Projet

```
.gitignore
app.py
bond.py
courbe_taux.csv
courbe_zero.py
README.md
requirements.txt
risque.py
```

- `app.py`: Le fichier principal de l'application Streamlit.
- `bond.py`: Contient la classe `Bond` pour la modélisation des obligations.
- `courbe_zero.py`: Contient la classe `ZeroCurve` pour la gestion de la courbe de taux zéro.
- `risque.py`: Contient les fonctions de calcul des métriques de risque (e.g., duration de Macaulay).
- `courbe_taux.csv`: Fichier CSV contenant les données de la courbe de taux zéro (tenors et rates).
- `requirements.txt`: Liste des dépendances Python nécessaires.
- `.gitignore`: Fichier pour ignorer les fichiers non pertinents pour Git.

## Configuration Locale

Suivez ces étapes pour exécuter l'application localement:

1.  **Clonez le dépôt GitHub** (une fois qu'il sera créé et pushé avec ces fichiers).

2.  **Créez et activez un environnement virtuel** (recommandé):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts ctivate`
    ```

3.  **Installez les dépendances nécessaires**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Lancez l'application Streamlit**:
    ```bash
    streamlit run app.py
    ```

L'application devrait s'ouvrir automatiquement dans votre navigateur web.

## Utilisation

- Utilisez la barre latérale pour ajuster les paramètres de l'obligation (Nominal, Taux de Coupon, Maturité, Fréquence des paiements).
- Le prix de l'obligation et sa duration de Macaulay seront affichés.
- La courbe de taux zéro utilisée pour les calculs est également visualisée.

## Déploiement sur Streamlit Community Cloud (ou autre plateforme)

Pour déployer cette application, vous aurez besoin des fichiers `app.py`, `bond.py`, `courbe_zero.py`, `risque.py`, `courbe_taux.csv`, et `requirements.txt` dans votre dépôt GitHub.

Les étapes générales pour le déploiement sur Streamlit Community Cloud sont les suivantes :

1.  Poussez votre code vers un dépôt GitHub.
2.  Connectez-vous à [Streamlit Community Cloud](https://share.streamlit.io/).
3.  Créez une nouvelle application et pointez-la vers votre dépôt GitHub, en spécifiant `app.py` comme fichier principal.

