# Application d'Analyse de Données avec Streamlit

## 📊 Aperçu du Projet
Cette application web interactive permet d'analyser et de visualiser des données à l'aide de Streamlit. Elle offre une interface utilisateur intuitive pour explorer les données, générer des graphiques et obtenir des insights pertinents.

## 🚀 Fonctionnalités
- Chargement et affichage des données
- Visualisations interactives
- Filtrage et exploration des données
- Génération de rapports

## 🛠️ Prérequis
- Python 3.8+
- pip (gestionnaire de paquets Python)

## 🚀 Installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/KalsoumDS/Streamlit-Data-Analysis-App.git
   cd Streamlit-Data-Analysis-App
   ```

2. Créez un environnement virtuel (recommandé) :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Lancement de l'Application
```bash
streamlit run Application.py
```

L'application sera disponible à l'adresse : http://localhost:8501

## 📂 Structure du Projet
```
Streamlit-Data-Analysis-App/
├── Application.py       # Code principal de l'application
├── pydb.csv            # Fichier de données
├── requirements.txt    # Dépendances Python
└── README.md           # Ce fichier
```

## 📊 Jeu de Données
L'application utilise un jeu de données stocké dans `pydb.csv`. Assurez-vous que ce fichier est présent dans le même répertoire que `Application.py`.

## 📝 Licence
Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
