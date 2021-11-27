import numpy as np
from matplotlib import pyplot as plt

def get_dataset(): 
    """
        Construire une dataset
    """

    # 5 malades et 5 en bonnes santé
    row_per_class = 100

    # On crée des valeurs arbitraires pour des caractéristiques type 'malade' et
    # 'bonne santé' volontairement écartées les unes des autres 
    sick = np.random.randn(row_per_class, 2) + np.array([-1,-1]) 
    healthy = np.random.randn(row_per_class, 2) + np.array([2,2]) 

    # On réuni toutes les entrées 
    # On associe à chaque entrée 0 (sick) ou 1(healthy)
    # On sait de manière certaines les états de chaque personne 
    features = np.vstack([sick, healthy]) 
    targets = np.concatenate((np.zeros(row_per_class), np.zeros(row_per_class) +1))

    return features, targets 

def init_variables(): 
    """
        On considère un seul neurone à deux entrées pondérées et un biais 
    """

    weights = np.random.uniform(size=2) 
    bias = 0 

    return weights, bias 

def pre_activation(features, weights, bias): 
    """
        retourne la valeur de la préactivation du neurone
        elle est dépendante de la valeur des poids, d'ou le backward pour les ajuster
    """
    return np.dot(features, weights) + bias 

def activation(z): 
    """
        L'activation résulte de l'application de la sigmoid 
        qui réduit l'amplitude à l'intervalle [0,1] 
    """

    return 1/(1+np.exp(-z))

def activation_derivative(z):
    """
        retourne la dérivée de la sigmoid, calculable à la main
    """

    return activation(z)*(1-activation(z))

def predict(features, weights, bias): 
    """
        Donne une prédiction {0,1} des targets associés à des features
    """

    # On donne la valeur 
    z = pre_activation(features, weights, bias) 
    y = activation(z) 

    return np.round(y)

def cost(predictions, targets): 
    """
        retourne l'erreur moyenne des predictions par rapport aux attendus 'targets'
    """

    return np.mean((predictions - targets)**2)

def train(features, targets, weights, bias): 
    """
        Regle les poids associés au modèle
    """

    epochs = 100
    learning_rate = 0.1

    # Donner une valeur de précision initiale de la prédiction 
    prediction = predict(features, weights, bias)
    print("Précision : ", np.mean(prediction == targets))

    # Affichage 
    plt.scatter(features[:, 0], features[:, 1], s=40, c=targets, cmap=plt.cm.Spectral) 
    plt.show()

    for epoch in range(epochs): 
        if epoch%10 == 0: 
            predictions = activation(pre_activation(features, weights, bias))
            print("Cost : %s" %cost(predictions, targets))
            
        # Initialise les gradients
        weights_gradients = np.zeros(weights.shape) 
        bias_gradient = 0

        for feature, target in zip(features, targets): 
            
            # calcule de la pré-activation & activation pour chaque couple (feature,target) 
            z = pre_activation(feature, weights, bias)
            y = activation(z) 

            # Mise à jour des gradients
            weights_gradients += (y-target)*activation_derivative(z)*feature
            bias_gradient += (y-target)*activation_derivative(z) 

        # Descente du gradient
        weights = weights - learning_rate*weights_gradients
        bias = bias - learning_rate*bias_gradient

    # Précision finale
    prediction = predict(features, weights, bias)
    print("Précision : ", np.mean(prediction == targets))



if __name__ == '__main__':

    # Etablir la dataset
    features, targets = get_dataset()

    # Initialiser le neurone
    weights, bias = init_variables()

    # Entrainer notre modèle
    train(features, targets, weights, bias)
