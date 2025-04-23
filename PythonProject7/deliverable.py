

# Esta función busca la primera palabra que empiece por una letra dada
# y la imprime al revés
def palabra_invertida(frase, letra):
   palabras = frase.split(" ")
   num = 0
   encontrada = False
   while num < len(palabras) and not encontrada:
       palabra = palabras[num]
       if palabra.startswith(letra):
           # Imprimir palabra al revés
           pos = len(palabra) - 1
           nueva = ""
           while pos >= 0:
               nueva = nueva + palabra[pos]
               pos = pos - 1
           print(nueva)
           encontrada = True
       num = num + 1


# Programa principal
frase = "Esta es una frase de ejemplo"
caracter = "f"


print("Buscando palabra que empiece con la letra:", caracter)
palabra_invertida(frase, caracter)



