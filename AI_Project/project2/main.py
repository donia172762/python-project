import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# === 1. إعداد المسار والبيانات ===
dataset_path = "."  # إذا كنت داخل نفس مجلد الصور
image_size = (32, 32)
data = []
labels = []

# === 2. قراءة الفئات ===
class_names = sorted([cls for cls in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, cls))])

# === 3. تحميل الصور وتحويلها إلى فيكتور ===
for label, class_name in enumerate(class_names):
    class_dir = os.path.join(dataset_path, class_name)
    for file in os.listdir(class_dir):
        file_path = os.path.join(class_dir, file)
        img = cv2.imread(file_path)
        if img is not None:
            img = cv2.resize(img, image_size)
            img = img.flatten()
            data.append(img)
            labels.append(label)

# === 4. تحويل البيانات إلى numpy arrays وتطبيق normalization ===
X = np.array(data) / 255.0  # Normalization
y = np.array(labels)

# === 5. طباعة معلومات الداتا ===
print("\n" + "=" * 50)
print("✅ Dataset Loaded Successfully!")
print(f"📦 Total Images        : {len(X)}")
print(f"🖼️ Image Flatten Size   : {X.shape[1]} pixels ({image_size[0]}x{image_size[1]}x3)")
print(f"🔢 Number of Classes    : {len(class_names)}")
print(f"🏷️ Class Labels         : {class_names}")
print("=" * 50 + "\n")

# === 6. تقسيم البيانات ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# === 7. تدريب نموذج Naive Bayes ===
print("\n🤖 Training Naive Bayes Classifier...")
nb_model = GaussianNB()
nb_model.fit(X_train, y_train)

# === 8. التنبؤ بالنتائج ===
y_pred_nb = nb_model.predict(X_test)

# === 9. تقييم النموذج ===
nb_accuracy = accuracy_score(y_test, y_pred_nb)
nb_report = classification_report(y_test, y_pred_nb, target_names=class_names)
nb_conf_matrix = confusion_matrix(y_test, y_pred_nb)

print("\n" + "=" * 50)
print("📊 Naive Bayes Classification Results")
print(f"✅ Accuracy: {nb_accuracy * 100:.2f}%")
print("\n🧾 Classification Report:\n")
print(nb_report)
print("=" * 50)

# === 10. رسم مصفوفة الالتباس ===
plt.figure(figsize=(6, 5))
sns.heatmap(nb_conf_matrix, annot=True, fmt="d", cmap="Blues",
            xticklabels=class_names, yticklabels=class_names)
plt.title("Confusion Matrix - Naive Bayes")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

# === 11. تدريب نموذج Decision Tree (معدل) ===
print("\n🌳 Training Decision Tree Classifier...")
dt_model = DecisionTreeClassifier(max_depth=10, min_samples_split=5, random_state=42)
dt_model.fit(X_train, y_train)

# === 12. التنبؤ بالنتائج ===
y_pred_dt = dt_model.predict(X_test)

# === 13. تقييم النموذج ===
dt_accuracy = accuracy_score(y_test, y_pred_dt)
dt_report = classification_report(y_test, y_pred_dt, target_names=class_names)
dt_conf_matrix = confusion_matrix(y_test, y_pred_dt)

print("\n" + "=" * 50)
print("🌳 Decision Tree Classification Results")
print(f"✅ Accuracy: {dt_accuracy * 100:.2f}%")
print("\n🧾 Classification Report:\n")
print(dt_report)
print("=" * 50)

# === 14. رسم مصفوفة الالتباس ===
plt.figure(figsize=(6, 5))
sns.heatmap(dt_conf_matrix, annot=True, fmt="d", cmap="YlGnBu",
            xticklabels=class_names, yticklabels=class_names)
plt.title("Confusion Matrix - Decision Tree")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

# === 15. تدريب نموذج MLP Neural Network ===
print("\n🧠 Training MLP Neural Network Classifier...")
mlp_model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=300, random_state=42)
mlp_model.fit(X_train, y_train)

# === 16. التنبؤ بالنتائج ===
y_pred_mlp = mlp_model.predict(X_test)

# === 17. تقييم النموذج ===
mlp_accuracy = accuracy_score(y_test, y_pred_mlp)
mlp_report = classification_report(y_test, y_pred_mlp, target_names=class_names)
mlp_conf_matrix = confusion_matrix(y_test, y_pred_mlp)

print("\n" + "=" * 50)
print("🧠 MLP Neural Network Classification Results")
print(f"✅ Accuracy: {mlp_accuracy * 100:.2f}%")
print("\n🧾 Classification Report:\n")
print(mlp_report)
print("=" * 50)

# === 18. رسم مصفوفة الالتباس ===
plt.figure(figsize=(6, 5))
sns.heatmap(mlp_conf_matrix, annot=True, fmt="d", cmap="Purples",
            xticklabels=class_names, yticklabels=class_names)
plt.title("Confusion Matrix - MLP Neural Network")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()
