import mondrianforest
import numpy as np
import pandas as pd


import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

APP_ENCODING = {'work': 0,'chrome': 1,'game': 2,'social_media': 3,'other': 4}

def loadModel():
    df = pd.read_csv('procrastination_data2.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['minute'] = df['timestamp'].dt.minute
    forest = mondrianforest.MondrianForestClassifier(n_tree=10)

    columns = ['mouse_clicks', 'hour', 'minute', 'feedback_response', 'keys_pressed', 'mouse_travel', 'tabs_changed',
               'app_focus_type']

    x = df[columns].to_numpy(dtype=np.float32)
    y = df['feedback_response'].to_numpy(dtype=np.int32)
    forest.fit(x, y)

    # Drop non-numeric or non-feature columns for modeling
    #X = df.drop(columns=['timestamp', 'feedback_response'])
    #y = df['feedback_response']  # Target variable

    #X_train, X_test, y_train, y_test = train_test_split(
    #   X, y, test_size=0.2, random_state=42, stratify=y
    #)
    for col in ['mouse_clicks', 'keys_pressed', 'mouse_travel', 'tabs_changed']:
        plt.figure(figsize=(10, 8))
        sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
        plt.title('Feature Correlation Heatmap')
        plt.show()

    #print(f"Training samples: {X_train.shape[0]}")
    #print(f"Testing samples: {X_test.shape[0]}")
    return forest

