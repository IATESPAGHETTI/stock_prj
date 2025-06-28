# ml_model.py
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

def train_and_evaluate(X, y, model_type='logistic'):
    # Time-based split to simulate realistic prediction
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    if model_type == 'logistic':
        model = LogisticRegression(max_iter=1000)
    else:
        model = DecisionTreeClassifier()

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    return model, accuracy
