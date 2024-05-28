import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import networkx as nx


# Definición de la clase para el nodo del árbol
class TreeNode:
    def __init__(self, student):
        self.student = student
        self.left = None
        self.right = None


# Definición de la clase para el árbol binario de búsqueda
class BinarySearchTree:
    def __init__(self):
        self.root = None

    # Método para agregar un estudiante al árbol
    def add_student(self, student):
        if not isinstance(student, Student):
            raise TypeError("El elemento debe ser un objeto de tipo Student")

        if not self.root:
            self.root = TreeNode(student)
        else:
            self._add_student_recursive(student, self.root)

    def _add_student_recursive(self, student, node):
        if student.id < node.student.id:
            if node.left is None:
                node.left = TreeNode(student)
            else:
                self._add_student_recursive(student, node.left)
        else:
            if node.right is None:
                node.right = TreeNode(student)
            else:
                self._add_student_recursive(student, node.right)

    # Método para buscar un estudiante en el árbol
    def find_student(self, student_id):
        return self._find_student_recursive(student_id, self.root)

    def _find_student_recursive(self, student_id, node):
        if node is None:
            return None
        if student_id == node.student.id:
            return node.student
        elif student_id < node.student.id:
            return self._find_student_recursive(student_id, node.left)
        else:
            return self._find_student_recursive(student_id, node.right)

    # Método para eliminar un estudiante del árbol
    def delete_student(self, student_id):
        self.root = self._delete_student_recursive(student_id, self.root)

    def _delete_student_recursive(self, student_id, node):
        if node is None:
            return node
        if student_id < node.student.id:
            node.left = self._delete_student_recursive(student_id, node.left)
        elif student_id > node.student.id:
            node.right = self._delete_student_recursive(student_id, node.right)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                temp = self._min_value_node(node.right)
                node.student = temp.student
                node.right = self._delete_student_recursive(temp.student.id, node.right)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    # Método para obtener la lista de estudiantes en orden ascendente según sus IDs
    def get_students_in_order(self):
        students = []
        self._get_students_in_order_recursive(self.root, students)
        return students

    def _get_students_in_order_recursive(self, node, students):
        if node is not None:
            self._get_students_in_order_recursive(node.left, students)
            students.append(node.student)
            self._get_students_in_order_recursive(node.right, students)


# Definición de la clase para representar a un estudiante
class Student:
    def __init__(self, id, name, age, number):
        self.id = id
        self.name = name
        self.age = age
        self.number = number


# Función para mostrar las instrucciones
def show_instructions():
    instructions = """
    Instrucciones:
    1. Agregar Estudiante:
       - Ingresa el ID, Nombre, Edad y Número del estudiante en los campos proporcionados.
       - Haz clic en el botón "Agregar Estudiante" para agregar el estudiante al sistema.

    2. Buscar Estudiante:
       - Ingresa el ID del estudiante que deseas buscar en el campo proporcionado.
       - Haz clic en el botón "Buscar Estudiante" para buscar al estudiante en el sistema.

    3. Eliminar Estudiante:
       - Ingresa el ID del estudiante que deseas eliminar en el campo proporcionado.
       - Haz clic en el botón "Eliminar Estudiante" para eliminar al estudiante del sistema.

    4. Mostrar Lista de Estudiantes:
       - Haz clic en el botón "Mostrar Lista de Estudiantes" para ver la lista de estudiantes registrados en orden ascendente según sus IDs.

    5. Mostrar Árbol:
       - Haz clic en el botón "Mostrar Árbol" para visualizar gráficamente el árbol binario de búsqueda que representa la organización de los estudiantes.
       - Para la grafica de arboles tiene botones abajo cada uno dice que hace en ingles solo fuen una libreria XD
    """
    messagebox.showinfo("Instrucciones", instructions)


# Función para mostrar una ventana con la lista de estudiantes
def show_students():
    students = tree.get_students_in_order()
    if students:
        student_list = "\n".join(
            [f"ID: {student.id}, Nombre: {student.name}, Edad: {student.age}, Número: {student.number}" for student in
             students])
        messagebox.showinfo("Lista de Estudiantes", student_list)
    else:
        messagebox.showinfo("Lista de Estudiantes", "No hay estudiantes registrados.")


# Función para agregar un estudiante
def add_student():
    try:
        id = int(id_entry.get())
        name = name_entry.get()
        age = int(age_entry.get())
        number = int(number_entry.get())

        new_student = Student(id, name, age, number)
        tree.add_student(new_student)

        messagebox.showinfo("Éxito", "Estudiante agregado correctamente.")

        id_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        number_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores válidos para ID, Edad y Número.")


# Función para buscar un estudiante
def find_student():
    try:
        id = int(id_entry.get())
        student = tree.find_student(id)
        if student:
            messagebox.showinfo("Estudiante Encontrado",
                                f"ID: {student.id}, Nombre: {student.name}, Edad: {student.age}, Número: {student.number}")
        else:
            messagebox.showinfo("Estudiante No Encontrado", f"No se encontró ningún estudiante con el ID {id}.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa un valor válido para el ID.")


# Resto del código aquí...

# Función para mostrar el árbol
def show_tree():
    if tree.root:
        G = nx.Graph()
        add_nodes(tree.root, G)
        add_edges(tree.root, G)
        pos = nx.spring_layout(G)
        plt.figure()
        nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=12, font_weight="bold")
        plt.title("Árbol Binario de Búsqueda de Estudiantes")
        plt.show()
    else:
        messagebox.showinfo("Árbol Vacío", "No hay estudiantes registrados para mostrar en el árbol.")


def add_nodes(node, G):
    if node:
        G.add_node(node.student.id)
        add_nodes(node.left, G)
        add_nodes(node.right, G)


def add_edges(node, G):
    if node:
        if node.left:
            G.add_edge(node.student.id, node.left.student.id)
        if node.right:
            G.add_edge(node.student.id, node.right.student.id)
        add_edges(node.left, G)
        add_edges(node.right, G)


# Función para eliminar un estudiante
def delete_student():
    try:
        id = int(id_entry.get())
        tree.delete_student(id)
        messagebox.showinfo("Éxito", f"Estudiante con ID {id} eliminado correctamente.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa un valor válido para el ID.")


# Creación de la ventana principal
root = tk.Tk()
root.title("Gestión de Almacenamiento de Estudiantes")

# Creación del árbol binario de búsqueda
tree = BinarySearchTree()

# Creación de los widgets
id_label = tk.Label(root, text="ID:")
id_entry = tk.Entry(root)
name_label = tk.Label(root, text="Nombre:")
name_entry = tk.Entry(root)
age_label = tk.Label(root, text="Edad:")
age_entry = tk.Entry(root)
number_label = tk.Label(root, text="Número:")
number_entry = tk.Entry(root)
add_button = tk.Button(root, text="Agregar Estudiante", command=add_student)
find_button = tk.Button(root, text="Buscar Estudiante", command=find_student)
delete_button = tk.Button(root, text="Eliminar Estudiante", command=delete_student)
show_button = tk.Button(root, text="Mostrar Lista de Estudiantes", command=show_students)
instructions_button = tk.Button(root, text="Mostrar Instrucciones", command=show_instructions)
tree_button = tk.Button(root, text="Mostrar Árbol", command=show_tree)

# Ubicación de los widgets en la ventana
id_label.grid(row=0, column=0, sticky="e")
id_entry.grid(row=0, column=1)
name_label.grid(row=1, column=0, sticky="e")
name_entry.grid(row=1, column=1)
age_label.grid(row=2, column=0, sticky="e")
age_entry.grid(row=2, column=1)
number_label.grid(row=3, column=0, sticky="e")
number_entry.grid(row=3, column=1)
add_button.grid(row=4, column=0, columnspan=2, pady=5)
find_button.grid(row=5, column=0, columnspan=2, pady=5)
delete_button.grid(row=6, column=0, columnspan=2, pady=5)
show_button.grid(row=7, column=0, columnspan=2, pady=5)
show_button.grid(row=7, column=0, columnspan=2, pady=5)
instructions_button.grid(row=8, column=0, columnspan=2, pady=5)
tree_button.grid(row=9, column=0, columnspan=2, pady=5)

# Ejecución de la ventana
root.mainloop()
