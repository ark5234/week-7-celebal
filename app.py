import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.datasets import load_iris
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix, roc_curve, auc

# Load model and feature names
def load_model():
    return joblib.load('models/iris_rf.pkl')

def get_feature_names():
    return load_iris().feature_names

def get_class_names():
    return load_iris().target_names

model = load_model()
feature_names = get_feature_names()
class_names = get_class_names()

st.set_page_config(page_title="Iris Species Predictor", page_icon="🌸", layout="centered")
st.title("🌸 Iris Species Predictor")
st.write("Input flower measurements to predict the Iris species using a Random Forest model.")

# Sidebar for user input
st.sidebar.header("Input Features")
user_input = {}
for feature in feature_names:
    min_val = float(load_iris().data[:, feature_names.index(feature)].min())
    max_val = float(load_iris().data[:, feature_names.index(feature)].max())
    mean_val = float(load_iris().data[:, feature_names.index(feature)].mean())
    user_input[feature] = st.sidebar.slider(
        feature.capitalize(), min_value=min_val, max_value=max_val, value=mean_val, step=0.1
    )

input_df = pd.DataFrame([user_input])

# Prediction
if st.button("Predict Species", type="primary"):
    prediction = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0]
    st.subheader(f"Prediction: :violet[{class_names[prediction].capitalize()}]")
    st.write("### Prediction Probabilities:")
    proba_df = pd.DataFrame({
        'Species': class_names,
        'Probability': proba
    })
    bar_data = proba_df.set_index('Species')
    if hasattr(bar_data, 'to_pandas'):
        bar_data = bar_data.to_pandas()
    st.bar_chart(bar_data)

    # Feature importance
    st.write("### Feature Importance:")
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=False)
    fig = px.bar(importance_df, x='Importance', y='Feature', orientation='h', title='Feature Importance')
    st.plotly_chart(fig, use_container_width=True)

# Show input values
with st.expander("Show input values"):
    st.write(input_df)

# --- New: Data Explorer Section ---
st.header("🔍 Iris Dataset Explorer")
iris = load_iris()
iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
iris_df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
st.dataframe(iris_df, use_container_width=True)

# --- New: Confusion Matrix Section ---
st.header("📊 Model Confusion Matrix (Test Data)")
# Split data for evaluation
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.3, random_state=42)
y_pred = model.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
cm_df = pd.DataFrame(cm, index=iris.target_names, columns=iris.target_names)
st.write("Confusion Matrix:")
st.dataframe(cm_df)
fig_cm = px.imshow(cm, text_auto=True, x=iris.target_names, y=iris.target_names, color_continuous_scale='Blues', title="Confusion Matrix")
st.plotly_chart(fig_cm, use_container_width=True)

# --- New: ROC Curve Section ---
st.header("📈 ROC Curves (One-vs-Rest)")
from sklearn.preprocessing import label_binarize
# Binarize the output for multi-class ROC
n_classes = len(iris.target_names)
y_test_bin = label_binarize(y_test, classes=range(n_classes))
y_score = model.predict_proba(X_test)
fig_roc = go.Figure()
for i in range(n_classes):
    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_score[:, i])
    roc_auc = auc(fpr, tpr)
    fig_roc.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', name=f"{iris.target_names[i]} (AUC={roc_auc:.2f})"))
fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', line=dict(dash='dash'), showlegend=False, marker_color='gray'))
fig_roc.update_layout(title="ROC Curves (One-vs-Rest)", xaxis_title="False Positive Rate", yaxis_title="True Positive Rate", width=700, height=500)
st.plotly_chart(fig_roc, use_container_width=True)

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | [GitHub](https://github.com/yourusername/your-repo)") 