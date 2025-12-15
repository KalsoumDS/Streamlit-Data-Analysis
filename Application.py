import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Config page
st.set_page_config(page_title="Analyse des Données AVC", layout="wide")

# Chargement des données (fichier local ou upload)
def load_data():
    try:
        return pd.read_csv("pydb.csv", header=0, index_col=0)
    except FileNotFoundError:
        st.warning("Fichier pydb.csv introuvable. Importez un CSV pour continuer.")
        uploaded = st.file_uploader("Choisir un CSV", type=["csv"])
        if uploaded:
            return pd.read_csv(uploaded, header=0, index_col=0)
        st.stop()

df = load_data()

# Prétraitement
df["bmi"] = df["bmi"].fillna(df["bmi"].median())
df["avg_glucose_level"] = df["avg_glucose_level"].fillna(df["avg_glucose_level"].mean())
df_encoded = pd.get_dummies(
    df,
    columns=["gender", "ever_married", "work_type", "Residence_type", "smoking_status"],
    drop_first=True,
)

# Suppression des outliers
def remove_outliers(df_in, column):
    Q1 = df_in[column].quantile(0.25)
    Q3 = df_in[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df_in[(df_in[column] >= lower_bound) & (df_in[column] <= upper_bound)]

df_cleaned = remove_outliers(df_encoded, "bmi")
df_cleaned = remove_outliers(df_cleaned, "avg_glucose_level")
df_cleaned = remove_outliers(df_cleaned, "age")

# Normalisation
scaler = StandardScaler()
df_cleaned[["age", "bmi", "avg_glucose_level"]] = scaler.fit_transform(
    df_cleaned[["age", "bmi", "avg_glucose_level"]]
)

# Menu
menu = st.sidebar.selectbox(
    "Menu",
    [
        "Distribution des variables continues",
        "Matrice de corrélation",
        "Comparaison des variables continues par AVC",
        "Répartition des variables catégoriques",
        "Boxplots des variables continues",
        "Distribution des variables par statut AVC",
    ],
)

# Vues
if menu == "Distribution des variables continues":
    st.header("Distribution des variables continues")
    variables = ["age", "avg_glucose_level", "bmi"]
    titles = ["Âge", "Glycémie Moyenne", "IMC"]

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    for i, var in enumerate(variables):
        sns.histplot(df_cleaned[var], kde=True, bins=30, ax=axes[i], color="blue", alpha=0.7)
        axes[i].set_title(f"Distribution de {titles[i]}")
    st.pyplot(fig)

elif menu == "Matrice de corrélation":
    st.header("Matrice de corrélation")
    df_numeric = df.select_dtypes(include=["float64", "int64"])
    corr_matrix = df_numeric.corr()

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
    ax.set_title("Matrice de Corrélation entre les Variables Numériques")
    st.pyplot(fig)

elif menu == "Comparaison des variables continues par AVC":
    st.header("Comparaison des variables continues par AVC")
    variables = ["age", "avg_glucose_level", "bmi"]
    titles = ["Âge", "Glycémie Moyenne", "IMC"]

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    for i, var in enumerate(variables):
        sns.boxplot(x="stroke", y=var, data=df, ax=axes[i])
        axes[i].set_title(f"Comparaison de {titles[i]} selon le statut AVC")
    st.pyplot(fig)

elif menu == "Répartition des variables catégoriques":
    st.header("Répartition des variables catégoriques")
    categorical_variables = ["gender", "ever_married", "work_type", "Residence_type", "smoking_status"]

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.flatten()
    for i, var in enumerate(categorical_variables):
        sns.countplot(x=var, hue="stroke", data=df, ax=axes[i])
        axes[i].set_title(f"Répartition de {var} selon le statut AVC")
    st.pyplot(fig)

elif menu == "Boxplots des variables continues":
    st.header("Boxplots des variables continues")
    variables = ["age", "avg_glucose_level", "bmi"]
    titles = ["Âge", "Glycémie Moyenne", "IMC"]

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    for i, var in enumerate(variables):
        sns.boxplot(x=df_cleaned[var], ax=axes[i])
        axes[i].set_title(f"Boxplot de {titles[i]}")
    st.pyplot(fig)

elif menu == "Distribution des variables par statut AVC":
    st.header("Distribution des variables par statut AVC")
    variables = {
        "Âge": "age",
        "Glycémie Moyenne": "avg_glucose_level",
        "IMC": "bmi",
    }

    for title, var in variables.items():
        fig, ax = plt.subplots(figsize=(18, 6))
        sns.histplot(df_cleaned[df_cleaned["stroke"] == 1][var], color="red", label="AVC", kde=True, bins=30, ax=ax)
        sns.histplot(df_cleaned[df_cleaned["stroke"] == 0][var], color="blue", label="Pas d'AVC", kde=True, bins=30, ax=ax)
        ax.set_title(f"Distribution de {title} selon le Statut AVC")
        ax.set_xlabel(title)
        ax.set_ylabel("Fréquence")
        ax.legend()
        st.pyplot(fig)
