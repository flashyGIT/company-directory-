class EmployeeNode:
    '''
    A class to represent a node in the binary tree.
    Attributes:
        name (str): The name of the employee.
        left (EmployeeNode): The left child node.
        right (EmployeeNode): The right child node.
    '''

    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None


class TeamTree:
    '''
    A class to represent a binary tree for managing a team structure.
    '''

    def __init__(self):
        self.root = None

    def insert(self, manager_name, employee_name, side, current_node=None):
        '''
        Recursively inserts an employee under the specified manager.
        The employee is added to the manager's LEFT or RIGHT position.
        '''

        if self.root is None:
            print("⚠️ Add a team lead before adding employees.")
            return False

        if side not in ("left", "right"):
            print("❌ Invalid side. Choose LEFT or RIGHT.")
            return False

        # Start at the root on the first call.
        if current_node is None:
            current_node = self.root

        # Found the manager.
        if current_node.name.lower() == manager_name.lower():
            if side == "left":
                if current_node.left is not None:
                    print(f"⚠️ {manager_name} already has a LEFT employee.")
                    return False
                current_node.left = EmployeeNode(employee_name)
            else:
                if current_node.right is not None:
                    print(f"⚠️ {manager_name} already has a RIGHT employee.")
                    return False
                current_node.right = EmployeeNode(employee_name)

            print(
                f"✅ {employee_name} added as the {side.upper()} "
                f"employee under {manager_name}."
            )
            return True

        # Recursively search the left subtree.
        if self.insert_in_subtree_exists(current_node.left, manager_name):
            return self.insert(
                manager_name, employee_name, side, current_node.left
            )

        # Recursively search the right subtree.
        if self.insert_in_subtree_exists(current_node.right, manager_name):
            return self.insert(
                manager_name, employee_name, side, current_node.right
            )

        # If the manager is not below this node, search the remaining tree
        # through the recursive traversal below.
        return self._insert_recursive(
            manager_name, employee_name, side, current_node
        )

    def insert_in_subtree_exists(self, node, manager_name):
        """Recursively checks whether a manager exists in a subtree."""
        if node is None:
            return False
        if node.name.lower() == manager_name.lower():
            return True
        return (
            self.insert_in_subtree_exists(node.left, manager_name)
            or self.insert_in_subtree_exists(node.right, manager_name)
        )

    def _insert_recursive(self, manager_name, employee_name, side, node):
        """Recursively searches for the manager and inserts the employee."""
        if node is None:
            return False

        if node.name.lower() == manager_name.lower():
            if side == "left":
                if node.left is not None:
                    print(f"⚠️ {manager_name} already has a LEFT employee.")
                    return False
                node.left = EmployeeNode(employee_name)
            else:
                if node.right is not None:
                    print(f"⚠️ {manager_name} already has a RIGHT employee.")
                    return False
                node.right = EmployeeNode(employee_name)

            print(f"✅ {employee_name} added under {manager_name}.")
            return True

        if self._insert_recursive(
            manager_name, employee_name, side, node.left
        ):
            return True

        if self._insert_recursive(
            manager_name, employee_name, side, node.right
        ):
            return True

        if node is self.root:
            print(f"❌ Manager '{manager_name}' was not found.")

        return False

    def print_tree(self, node=None, level=0):
        '''
        Recursively prints the team structure.
        Right employees appear above the manager, and left employees below.
        '''

        # Allow print_tree() to start at the root.
        if node is None:
            if level == 0:
                node = self.root
            else:
                return

        if node is None:
            print("⚠️ The team structure is empty.")
            return

        # Print the right subtree first.
        self.print_tree(node.right, level + 1)

        # Print the current employee.
        print("    " * level + f"└── {node.name}")

        # Print the left subtree.
        self.print_tree(node.left, level + 1)


# CLI functionality
def company_directory():
    tree = TeamTree()

    while True:
        print("\n📋 Team Management Menu")
        print("1. Add Team Lead (root)")
        print("2. Add Employee")
        print("3. Print Team Structure")
        print("4. Exit")

        choice = input("Choose an option (1–4): ").strip()

        if choice == "1":
            if tree.root:
                print("⚠️ Team lead already exists.")
            else:
                name = input("Enter team lead's name: ").strip()
                if name:
                    tree.root = EmployeeNode(name)
                    print(f"✅ {name} added as the team lead.")
                else:
                    print("❌ Name cannot be empty.")

        elif choice == "2":
            manager = input("Enter the manager's name: ").strip()
            employee = input("Enter the new employee's name: ").strip()
            side = input(
                "Should this employee be on the LEFT or RIGHT of the manager? "
            ).strip().lower()

            if not manager or not employee:
                print("❌ Manager and employee names cannot be empty.")
            elif manager.lower() == employee.lower():
                print("❌ An employee cannot report to themselves.")
            else:
                tree.insert(manager, employee, side)

        elif choice == "3":
            print("\n🌳 Current Team Structure:")
            tree.print_tree()

        elif choice == "4":
            print("Good Bye!")
            break

        else:
            print("❌ Invalid option. Try again.")


if __name__ == "__main__":
    company_directory()   

#DESIGN MEMO: Employee Reporting Hierarchy

#Purpose:
#This program models a company's employee reporting structure using a
#binary tree. It provides a simple, interactive command-line interface
#for adding employees and displaying the organizational hierarchy.

#Design:
#The EmployeeNode class represents an individual employee. Each node
#stores the employee's name and references to two possible direct
#reports, left and right. The TeamTree class manages the overall
#structure, with the root representing the team lead or CEO.

#Recursive insertion searches for a specified manager and places a
#new employee in the requested left or right position. The program
#checks whether the manager exists and whether the selected position
#is already occupied. These checks prevent invalid insertions and
#ensure that each manager has no more than two direct reports.

#Recursive traversal displays the hierarchy in a readable tree format.
#The command-line interface provides options to add the root employee,
#add employees, display the structure, and exit the program.

#Scalability and Limitations:
#The recursive design makes the program easy to understand and extend.
#However, searching for managers requires traversing the tree, which
#can take O(n) time for n employees. A highly unbalanced tree may also
#increase recursion depth. Additionally, the binary-tree model limits
#each manager to two direct reports, unlike most real organizations.

#Future Improvements:
#Possible enhancements include employee deletion, searching, data
#persistence, duplicate-name validation, and support for multiple
#direct reports through a general tree structure.
#"""
