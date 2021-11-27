
if __name__ == '__main__': 

    # la fonction
    f = lambda x,y : 3*x**2 +x*y +5*y**2

    # les dérivées partielles d'une fonction
    partial_derivative_x = lambda x,y : 6*x +y
    partial_derivative_y = lambda x,y : x + 10*y 

    # on fixe le point initial 
    x = 10
    y = -13

    # on affiche la valeur de la fonction initialement
    print("F= %s" %f(x,y))

    # Le learning rate sert à ne pas diverger sur l'algo de descente de gradient
    learning_rate = 0.1

    # une epoch est une session de minimisation 
    for epoch in range(20): 

        # on actualise la valeur des variables 
        x = x - learning_rate*partial_derivative_x(x,y) 
        y = y - learning_rate*partial_derivative_y(x,y)

        # quelle valeur prend on sur la fonction ?
        # on cherche à approcher un minimum, préférentiellement global (ici 0)
        print("F= %s" %f(x,y))

    print("\nFinalement")
    print("x = %s" %x)
    print("y = %s" %y)