from operator import attrgetter

LETRAS = 26

class TCelda:
    def __init__(self, palabra, significado, sig):
        self.palabra = palabra
        self.significado = significado
        self.sig = sig

    def set_palabra(self, p):
        self.palabra = p

    def set_significado(self, s):
        self.significado = s

    def set_sig(self, ptr):
        self.sig = ptr

    def get_palabra(self):
        return self.palabra

    def get_significado(self):
        return self.significado

    def get_sig(self):
        return self.sig

def a_minuscula(word):
    return word.lower()

class Diccionario:
    def __init__(self):
        self.hashtable = []

    def insertar_palabra(self, palabra, significado):
        nuevo = TCelda(palabra, significado, None)
        self.hashtable.append(nuevo)
        return True

    def buscar_palabra(self, palabra_buscar):
        palabra_buscar = palabra_buscar.lower()

        for ptr in self.hashtable:
            
            #print(str(ptr.get_palabra()) + ", " + palabra_buscar)

            if ptr.get_palabra() == palabra_buscar:
                print(f"\n\t{ptr.get_palabra()}: {ptr.get_significado()}")
                return True

            ptr = ptr.get_sig()

        print("\tPalabra no encontrada...")
        return False

    def imprimir_todo(self):
        for i in range(LETRAS):
            car = chr(i + 97)
            cantidad = self.contar_palabra_letra(car)

            print(f"\n Letra: {car}")
            print(f" Número de palabras por la letra {car}: {cantidad}\n")

            if cantidad == 0:
                print(f" La letra {car} no tiene palabras registradas.")
            else:
                for word in self.hashtable:
                    if word.get_palabra()[0] == car:
                        print(f" {word.get_palabra()}: {word.get_significado()}")
        
        return True

    def imprimir_letra(self):
        buscar = ""

        while not buscar.isalpha() or len(buscar) != 1:
            buscar = input("\n¿Por qué letra desea imprimir las palabras almacenadas?: ").lower()

            if not buscar.isalpha() or len(buscar) != 1:
                print("\n¡Carácter ingresado no válido!\n")

        print()
        car = buscar
        cantidad = self.contar_palabra_letra(car)
        if cantidad == 0:
                print(f" La letra {car} no tiene palabras registradas.")
        else:
            for word in self.hashtable:
                if word.get_palabra()[0] == car:
                    print(f" {word.get_palabra()}: {word.get_significado()}")

        return True

    def contar_palabra_letra(self, l):
        acum = 0

        for word in self.hashtable:
            if(word.get_palabra()[0] == l):
                acum += 1


        return acum

    def ordernar(self):
        self.hashtable.sort(key=attrgetter('palabra'))

    def modificar_palabra(self, palabra, significado):
        if self.buscar_palabra(palabra):
            for word in self.hashtable:
                if word.get_palabra() == palabra:
                    word.set_sig(significado)

    def verificar_sobreescritura(self, palabra_buscar):
        palabra_buscar = palabra_buscar.lower()

        ptr = self.hashtable[ord(palabra_buscar[0]) - 97]

        while ptr is not None:
            if ptr.get_palabra() == palabra_buscar:
                return True

            ptr = ptr.get_sig()

        return False

class Archivo:
    def __init__(self):
        self.Lec = None
        self.Esc = None
    
    def cargar_diccionario(self, D):
        print("Cargando Archivos....")
        
        try:
            with open("diccionarioPrueba.txt", "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        nombre, definicion = line.split('].')
                        nombre = nombre[1:]
                        definicion = definicion.strip()
                        D.insertar_palabra(nombre, definicion)
        except IOError:
            print("\nError al abrir el archivo txt. Por favor, revise.")
            input()
            exit(1)

        return True
    
    def agregar_palabra(self, palabra, significado):
        with open("diccionarioPrueba.txt", "a") as file:
            file.write("\n[" + palabra + "]. " + significado)

        return True
    
    def eliminar_palabra(self,palabra):
        with open("diccionarioPrueba.txt", "r") as f:
            lines = f.readlines()

        with open("diccionarioPrueba.txt", "w") as f:
            for line in lines:
                line.strip()
                nombre, definicion = line.split("].")
                nombre = nombre[1:]

                if nombre != palabra:
                    f.write(line)
        
        return True
    
    def modificar_palabra(self, palabra, significado):
        with open("diccionarioPrueba.txt", "r") as f:
            data = f.readlines()

        for i in range(len(data)):
            nombre, definicion = data[i].split("].")
            nombre = nombre[1:]

            if nombre == palabra:
                print("linea a modificar: " + data[i])
                data[i] = "[" + palabra + "]. " + significado + "\n"

        with open('diccionarioPrueba.txt', 'w') as file:
            file.writelines(data)

    '''def ordernar(self):
        with open("diccionarioPrueba.txt", "r") as f:
            data = f.readlines()

        data.sort()

        with open('diccionarioPrueba.txt', 'w') as file:
            file.writelines(data)
    '''

def eliminar_palabra(A: Archivo, D: Diccionario):
    palabra_eliminar = input("\nQué palabra desea eliminar?: ").lower()
    D.eliminar_palabra(palabra_eliminar)
    A.eliminar_palabra(palabra_eliminar)
    print("Palabra eliminada con éxito...")
    input("Presione Enter para continuar")

def agregar_palabra_nueva(A: Archivo, D: Diccionario):
    while True:
        palabra_n = input("\nQué palabra desea agregar?: ").lower()
        if ord(palabra_n[0]) < 97 or ord(palabra_n[0]) > 122:
            print("\nLa primera letra de la palabra no es válida para su almacenamiento en el diccionario. Intente nuevamente.")
        else:
            if not D.verificar_sobreescritura(palabra_n):
                significado_n = input("Cuál es el significado de esa palabra?: ")
                significado_n = significado_n.capitalize()
                A.agregar_palabra(palabra_n, significado_n)
                D.insertar_palabra(palabra_n, significado_n)
                D.ordernar()
            else:
                print("La palabra ya existe en el diccionario...")
            break

def modificar_palabra(A: Archivo, D: Diccionario):
    palabra_modificar = input("Cuál palabra deseas modificar?: ")
    if D.buscar_palabra(palabra_modificar):
        significado = input("Digite significado modificado: ")

        D.modificar_palabra(palabra_modificar, significado)
        A.modificar_palabra(palabra_modificar, significado)

def menu(D: Diccionario, A: Archivo):
    while True:
        print("--DICCIONARIO--\n")
        print("Elija una opcion:\n")
        print("--VISUALIZAR--")
        print("1. Buscar palabra")
        print("2. Imprimir por letra")
        print("3. Imprimir palabras por orden alfabetico\n")
        print("--MODIFICAR--")
        print("4. Agregar")
        print("5. Modificar")
        print("6. Eliminar")
        print("0. Salir\n")
        opc = input("Opcion: ").upper()
        print()
        if opc == '1':
            palabra = input("Qué palabra desea buscar?: ")
            D.buscar_palabra(palabra)
            input("Presione Enter para continuar")
        elif opc == '2':
            D.imprimir_letra()
            input("Presione Enter para continuar")
        elif opc == '3':
            D.imprimir_todo()
            input("Presione Enter para continuar")
        elif opc == '4':
            agregar_palabra_nueva(A, D)
        elif opc == '5':
            modificar_palabra(A, D)
        elif opc == '6':
            eliminar_palabra(A, D)
        elif opc == '0':
            break
        else:
            print("Opción no válida.")
            input("Presione Enter para continuar")
        print()

def main():
    D = Diccionario()
    A = Archivo()
    A.cargar_diccionario(D)
    D.ordernar()
    #A.ordernar()

    menu(D, A)
    print("Gracias por usar nuestro diccionario....")

if __name__ == "__main__":
    main()


