from disease_classifier.data import load_golub
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report


def main() -> None:
    X, y = load_golub()
    # Split into training and testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)
    print("Test accuracy:", clf.score(X_test, y_test))

    y_pred = clf.predict(X_test)
    cm = confusion_matrix(y_test, y_pred, labels=["ALL", "AML"])
    print("Confusion matrix (rows = true, cols = pred):")
    print(cm)

    print(classification_report(y_test, y_pred, target_names=["ALL", "AML"]))


if __name__ == "__main__":
    main()