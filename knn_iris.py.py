import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris

# Inicialização do dataset
iris = load_iris()
X = iris.data
y = iris.target
target_names = list(iris.target_names)

# Função para adicionar nova amostra e re-treinar
def add_sample_and_retrain(X, y, target_names, new_sample, new_class_name):
    # Se a classe ainda não existe, adicione ao target_names
    if new_class_name not in target_names:
        target_names.append(new_class_name)
        new_class = len(target_names) - 1
    else:
        new_class = target_names.index(new_class_name)
    # Adiciona amostra e classe
    X = np.vstack([X, new_sample])
    y = np.append(y, [new_class])
    return X, y, target_names

# Exemplo de uso
new_sample = [6.0, 3.0, 5.0, 1.5]
new_class_name = 'rosa'

X, y, target_names = add_sample_and_retrain(X, y, target_names, new_sample, new_class_name)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"Acurácia do modelo: {accuracy * 100:.2f}%")

# Previsão
sample = np.array([new_sample]).reshape(1, -1)
prediction = model.predict(sample)
print("Classe prevista para a amostra:", target_names[prediction[0]])

# --- Para adicionar mais amostras:
# X, y, target_names = add_sample_and_retrain(X, y, target_names, [5.5, 3.1, 4.7, 1.2], 'rosa')
# (repita o treinamento após cada adição)