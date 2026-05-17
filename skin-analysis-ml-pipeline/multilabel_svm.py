#!/usr/bin/env python3
import os
import cv2
import numpy as np
import pandas as pd
import joblib
import warnings
from sklearn.exceptions import UndefinedMetricWarning
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, f1_score, hamming_loss

warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

MODEL_PATH = "svm_multilabel.pkl"

def load_data(csv_path, img_dir=None):
    df = pd.read_csv(csv_path)
    base_dir = img_dir if img_dir else os.path.dirname(csv_path) or '.'
    image_paths = [os.path.join(base_dir, f) for f in df['filename']]
    labels = df.drop(columns=['filename'])
    labels = labels.loc[:, labels.nunique() > 1]
    class_names = labels.columns.tolist()
    return image_paths, labels.values, class_names

def extract_features(img_paths, img_size=(64, 64)):
    images = []
    for path in img_paths:
        img = cv2.imread(path)
        if img is not None:
            img = cv2.resize(img, img_size)
            img = img.astype(np.float32) / 255.0
            img = img.flatten()
            images.append(img)
    features = np.array(images)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)
    return scaled, scaler

def train_svm(X_train, y_train, fast_mode=False, linear=True):
    kernel = 'linear' if linear else 'rbf'
    base_svm = SVC(kernel=kernel, probability=True, class_weight='balanced')

    if fast_mode:
        param_grid = {
            'estimator__C': [1, 10],
            'estimator__gamma': ['scale'] if not linear else ['auto']
        }
        cv_folds = 2
    else:
        param_grid = {
            'estimator__C': [0.01, 0.1, 1, 10, 100],
            'estimator__gamma': ['scale', 1, 0.1, 0.01, 0.001]
        }
        cv_folds = 3

    ovr = OneVsRestClassifier(base_svm)
    grid = GridSearchCV(ovr, param_grid, cv=cv_folds, scoring='f1_macro', verbose=2, n_jobs=-1)
    grid.fit(X_train, y_train)
    return grid.best_estimator_

def evaluate_model(clf, X_test, y_test, class_names):
    y_pred = clf.predict(X_test)

    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=class_names, zero_division=0))

    subset_acc = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average='macro')
    micro_f1 = f1_score(y_test, y_pred, average='micro')
    hamming = hamming_loss(y_test, y_pred)

    print("\n✅ Evaluation Metrics:")
    print(f"Subset Accuracy      : {subset_acc:.4f}")
    print(f"Macro F1 Score       : {macro_f1:.4f}")
    print(f"Micro F1 Score       : {micro_f1:.4f}")
    print(f"Hamming Loss         : {hamming:.4f}")

    print("\n📌 Per-Class Accuracy:")
    per_class_accuracies = []
    for i, name in enumerate(class_names):
        correct = np.sum(y_test[:, i] == y_pred[:, i])
        total = y_test.shape[0]
        acc = correct / total
        per_class_accuracies.append(acc)
        print(f"{name:20s}: {acc:.4f} ({correct}/{total})")

    avg_label_accuracy = np.mean(per_class_accuracies)
    print(f"\n🔢 Average Label Accuracy: {avg_label_accuracy:.4f}")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_path', nargs='?', default='images.v1i.multiclass/test/_classes.csv')
    parser.add_argument('--img-dir', type=str, default=None)
    parser.add_argument('--only-eval', action='store_true')
    parser.add_argument('--test-size', type=float, default=0.15)
    parser.add_argument('--val-size', type=float, default=0.15)
    parser.add_argument('--fast-mode', action='store_true')
    parser.add_argument('--linear', action='store_true', default=True)
    parser.add_argument('--limit', type=int, default=None)
    args = parser.parse_args()

    paths, labels, class_names = load_data(args.csv_path, img_dir=args.img_dir)

    if args.limit is not None:
        paths = paths[:args.limit]
        labels = labels[:args.limit]

    if args.only_eval:
        X, _ = extract_features(paths)
        loaded = joblib.load(MODEL_PATH)
        evaluate_model(loaded['model'], X, labels, loaded['class_names'])
        return

    train_paths, test_paths, y_train, y_test = train_test_split(paths, labels, test_size=args.test_size, random_state=42)
    train_paths, val_paths, y_train, y_val = train_test_split(train_paths, y_train, test_size=args.val_size / (1 - args.test_size), random_state=42)

    X_train, scaler = extract_features(train_paths)
    X_val, _ = extract_features(val_paths)
    X_test, _ = extract_features(test_paths)

    clf = train_svm(X_train, y_train, fast_mode=args.fast_mode, linear=args.linear)
    joblib.dump({'model': clf, 'class_names': class_names, 'scaler': scaler}, MODEL_PATH)

    evaluate_model(clf, X_test, y_test, class_names)

if __name__ == '__main__':
    main()
