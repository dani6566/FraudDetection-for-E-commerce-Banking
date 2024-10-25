# Function to evaluate model performance
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_pred_classes = (y_pred > 0.5).astype(int)  # Thresholding for binary classification
    print(classification_report(y_test, y_pred_classes))
    print("Accuracy:", accuracy_score(y_test, y_pred_classes))