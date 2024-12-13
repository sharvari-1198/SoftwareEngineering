import matplotlib.pyplot as plt
import networkx as nx

# Class to represent a node in the AVL Tree
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # Height of the node for balancing

# AVL Tree class
class AVLTree:
    # Function to get the height of a node
    def get_height(self, node):
        if not node:
            return 0
        return node.height

    # Function to get the balance factor of a node
    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    # Right rotate function for balancing
    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1

        # Return new root
        return x

    # Left rotate function for balancing
    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1

        # Return new root
        return y

    # Function to insert a node into the AVL tree
    def insert(self, node, key):
        # Step 1: Perform normal BST insert
        if not node:
            return Node(key)
        elif key < node.key:
            node.left = self.insert(node.left, key)
        else:
            node.right = self.insert(node.right, key)

        # Step 2: Update height of this ancestor node
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # Step 3: Get the balance factor of this node to check if it is unbalanced
        balance = self.get_balance(node)

        # Step 4: If the node is unbalanced, then balance it using rotations

        # Left Left Case
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)

        # Right Right Case
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)

        # Left Right Case
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right Left Case
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        # Return the (unchanged) node pointer
        return node

    # Function to perform an in-order traversal of the tree
    def in_order_traversal(self, node):
        if node:
            self.in_order_traversal(node.left)
            print(node.key, end=' ')
            self.in_order_traversal(node.right)

    # Function to visualize the tree using Matplotlib
    def visualize_tree(self, node, pos=None, level=0, width=2., vert_gap=0.4, xcenter=0.5):
        if pos is None:
            pos = {node.key: (xcenter, 1 - level * vert_gap)}

        # Offset for the next nodes
        offset = width / 2 ** (level + 1)
        if node.left is not None:
            xcenter -= offset
            pos[node.left.key] = (xcenter, 1 - (level + 1) * vert_gap)
            self.visualize_tree(node.left, pos, level + 1, width, vert_gap, xcenter)
            xcenter += offset

        if node.right is not None:
            xcenter += offset
            pos[node.right.key] = (xcenter, 1 - (level + 1) * vert_gap)
            self.visualize_tree(node.right, pos, level + 1, width, vert_gap, xcenter)

        return pos

    # Function to generate the tree visualization using NetworkX
    def draw_tree(self, node):
        pos = self.visualize_tree(node)
        plt.figure(figsize=(12, 8))
        nx_graph = nx.Graph()
        
        # Add nodes to the graph
        for key, value in pos.items():
            nx_graph.add_node(key, pos=value)

        # Add edges for the graph based on tree structure
        def add_edges(n):
            if n:
                if n.left:
                    nx_graph.add_edge(n.key, n.left.key)
                    add_edges(n.left)
                if n.right:
                    nx_graph.add_edge(n.key, n.right.key)
                    add_edges(n.right)

        add_edges(node)

        # Draw the tree with labels
        nx.draw(nx_graph, pos, with_labels=True, arrows=True, node_size=2000, node_color="lightblue", font_size=15, font_weight="bold")
        plt.title("AVL Tree Visualization")
        plt.show()


# Main function to take user input and build AVL tree
def main():
    avl_tree = AVLTree()
    root = None

    while True:
        print("\nMenu:")
        print("1. Insert a node")
        print("2. Delete a node")
        print("3. Search for a node")
        print("4. Display In-order traversal")
        print("5. Exit")

        choice = int(input("Enter your choice (1-5): "))

        if choice == 1:
            key = int(input("Enter the value to insert: "))
            root = avl_tree.insert(root, key)
            print(f"Inserted {key} into the AVL Tree.")
        elif choice == 2:
            key = int(input("Enter the value to delete: "))
            root, deleted = avl_tree.delete(root, key)  # Capture both root and deletion status

            if deleted != -1:
                print(f"Deleted {key} from the AVL Tree.")
        elif choice == 3:
            key = int(input("Enter the value to search: "))
            result = avl_tree.search(root, key)
            if result:
                print(f"Node {key} found in the AVL Tree.")
            else:
                print(f"Node {key} not found in the AVL Tree.")
        elif choice == 4:
            print("In-order Traversal of AVL Tree:")
            avl_tree.inorder_traversal(root)
            print()
        elif choice == 5:
            print("Exiting program.")
            break
        else:
            print("Invalid choice! Please select a valid option.")

main()
