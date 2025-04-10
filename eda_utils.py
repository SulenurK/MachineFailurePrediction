# -*- coding: utf-8 -*-
"""eda_utils.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RgyRp1e7qFq6Uv13H9Eptj3_68aOXEvk
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

# Function to split feature and target columns and optionally normalize numeric features
def split_feature_cols(df, id_cols, target_col=None, normalize=False):
    """
    Split the DataFrame into features and target, also separating numeric and categorical features.

    Parameters:
    - df: Input DataFrame
    - id_cols: Number of ID columns to drop from the left
    - target_col: Name of the target column (defaults to last column if None)
    - normalize: If True, numeric features will be normalized using MinMaxScaler

    Returns:
    - feature_df: DataFrame with only feature columns (normalized if requested)
    - features_target_df: DataFrame with features + target (for reference)
    - num_cols: List of numeric column names
    - cat_cols: List of categorical column names
    - feature_cols: List of all feature column names
    """
    features_target_df = df.iloc[:, id_cols:]
    if target_col is None:
        target_col = df.columns[-1]
    feature_df = features_target_df.drop(columns=[target_col])
    num_cols = feature_df.select_dtypes(include=['float64', 'int64']).columns
    cat_cols = feature_df.select_dtypes(include=['object']).columns
    feature_cols = feature_df.columns

    if normalize:
        scaler = MinMaxScaler()
        feature_df[num_cols] = scaler.fit_transform(feature_df[num_cols])

    return feature_df, features_target_df, num_cols, cat_cols, feature_cols

# Draw histograms for numeric columns with optional grouping and density option
def draw_histograms(dataframe, feature_columns, hue=None, bins=50, dimension=(6, 4), density=False):
    for col in feature_columns:
        plt.figure(figsize=dimension)
        if hue:
            sns.histplot(data=dataframe, x=col, hue=hue, bins=bins, kde=False,
                         palette='viridis', edgecolor='#D3D3D3', stat='density' if density else 'count')
        else:
            plt.hist(dataframe[col], bins=bins, color='#4682B4', edgecolor='#D3D3D3', density=density)

        plt.title(f'Histogram of {col}' + (f' by {hue}' if hue else ''))
        plt.xlabel(col)
        plt.ylabel('Density' if density else 'Frequency')
        plt.grid(True, linestyle='--', alpha=0.8)
        plt.show()

# Draw boxplots for numeric columns
def draw_boxplots(dataframe, numeric_cols):
    color = '#1f4591'
    for col in numeric_cols:
        plt.figure(figsize=(4, 4))
        sns.boxplot(data=dataframe[col], color=color, flierprops={'marker': 'o', 'markersize': 3})
        plt.title(f"Boxplot of {col}")
        plt.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
        plt.show()

# Draw a pairplot for numeric columns colored by target
def draw_pairplot(df, target_col):
    sns.pairplot(df, hue=target_col)
    plt.show()

# Draw a correlation heatmap for numeric features
def draw_heatmap(df):
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap='crest')
    plt.title("Correlation Heatmap")
    plt.show()

# Plot bar charts for all categorical features with optional normalization and hue
def plot_all_barcharts(data, hue=None, normalize=False, dimension=(10, 6)):
    for column in data.columns:
        if pd.api.types.is_numeric_dtype(data[column]):
            continue

        plt.figure(figsize=dimension)

        if normalize:
            if hue:
                grouped_data = data.groupby([column, hue]).size().unstack()
                grouped_data = grouped_data.div(grouped_data.sum(axis=1), axis=0)
                grouped_data.plot(kind='bar', stacked=True, figsize=dimension)
                plt.ylabel('Normalized Count')
            else:
                counts = data[column].value_counts(normalize=True)
                sns.barplot(x=counts.index, y=counts.values, order=counts.index)
                plt.ylabel('Normalized Count')
        else:
            sns.countplot(x=data[column], hue=hue, data=data)
            plt.ylabel('Count')

        plt.title(f'Bar Chart of {column}' + (f' by {hue}' if hue else ''))
        plt.xlabel(column)
        plt.xticks(rotation=45)
        plt.show()

# Plot heatmaps for categorical feature combinations with optional normalization
def plot_categorical_heatmaps(df, col1=None, col2=None, normalization=None):
    cat_columns = df.select_dtypes(include=['object', 'category']).columns
    pairs = [(col1, col2)] if col1 and col2 else [(c1, c2) for i, c1 in enumerate(cat_columns) for c2 in cat_columns[i+1:]]

    for col1, col2 in pairs:
        cross_tab = pd.crosstab(df[col1], df[col2])

        if normalization == "row":
            cross_tab = cross_tab.div(cross_tab.sum(axis=1), axis=0)
        elif normalization == "column":
            cross_tab = cross_tab.div(cross_tab.sum(axis=0), axis=1)

        plt.figure(figsize=(8, 6))
        sns.heatmap(cross_tab, annot=True, cmap="coolwarm", fmt=".2f" if normalization else "d")
        plt.title(f"Heatmap of {col1} vs {col2} ({'No Normalization' if normalization is None else normalization.capitalize() + ' Normalization'})")
        plt.xlabel(col2)
        plt.ylabel(col1)
        plt.show()

# Analyze each categorical feature against the target with stacked histograms and counts
def plot_categorical_analysis(df, target_col):
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns
    categorical_columns = [col for col in categorical_columns if col != target_col]

    for col in categorical_columns:
        print(f"Analyzing column: {col}")

        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x=col, hue=target_col, multiple='stack', palette='viridis', stat='percent')
        plt.title(f'Distribution of {col} by {target_col}')
        plt.xticks(rotation=45)
        plt.show()

        value_counts = df.groupby(target_col)[col].value_counts()
        print(f"Value counts for {col} by {target_col}:")
        print(value_counts, "\n")