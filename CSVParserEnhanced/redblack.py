########################################################################
# Name        : Binary Search Tree Refactor
# Author      : Buddy Marcey
# Course      : CS499 Computer Science Capstone
# Date        : November 24, 2024,
# Version     : 1.0
# Description : Red-Black Binary Search Tree with data import feature
########################################################################

import csv

"""
Logic to make a red-black tree function properly, according to the CS300 zyBooks:
    The root node is black
    A red node's children cannot be red
    A null child is considered to be a black leaf node
    All paths from a node to any null leaf descendant node must have the same number
    of black nodes
"""
class Course:

    def __init__(self, courseid, name = None, prereq1 = None, prereq2 = None, prereq3 = None):
        self.courseid = courseid
        self.name = name
        self.prereq1 = prereq1
        self.prereq2 = prereq2
        self.prereq3 = prereq3

    def print_result(self):
        print(f"ID {self.courseid}")
        print(f"Name {self.name}")
        if self.prereq1:
            print(f"Prereq 1 {self.prereq1}")
        if self.prereq2:
            print(f"Prereq 2 {self.prereq2}")
        if self.prereq3:
            print(f"Prereq 3 {self.prereq3}")
        print()




# Red-Black tree implementation based on krishna_g's contribution found at
# https://www.geeksforgeeks.org/red-black-tree-in-python/
# First, we define a node: it will have a course, value, color, and pointers to children and parents
class Node:
    def __init__(self, value, course = None, color = 'red'):
        self.value = value
        self.course = course
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    #grandparent is needed for check to maintain color integrity
    def grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    # sibling is needed to check if rotation is needed
    def sibling(self):
        if self.parent is None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left

    # uncle used when color integrity needs to be fixed
    def uncle(self):
        if self.parent is None:
            return None
        return self.parent.sibling()

class RedBlackTree:

    def __init__(self):
        self.root = None

    # binary search: looks left if value less than current, otherwise right
    def search(self, value):
        curr_node = self.root
        while curr_node is not None:
            if value == curr_node.value:
                return curr_node
            elif value < curr_node.value:
                curr_node = curr_node.left
            else:
                curr_node = curr_node.right
        return None


    # like search finds proper slot for new node and inserts
    def insert(self, value, course):

        new_node = Node(value, course)
        if self.root is None:
            self.root = new_node
        else:
            curr_node = self.root
            while True:

                if value < curr_node.value:
                    if curr_node.left is None:
                        curr_node.left = new_node
                        new_node.parent = curr_node
                        break
                    else:
                        curr_node = curr_node.left

                else:
                    if curr_node.right is None:
                        curr_node.right = new_node
                        new_node.parent = curr_node
                        break
                    else:
                        curr_node = curr_node.right
        self.insert_fix(new_node)

    # this check is done after insertion to determine color integrity;
    # fix implemented if color integrity is invalid
    def insert_fix(self, new_node):

        while new_node.parent and new_node.parent.color == 'red':
            if new_node.parent == new_node.grandparent().left:
                uncle = new_node.uncle()
                if uncle and uncle.color == 'red':
                    new_node.parent.color = 'black'
                    uncle.color = 'black'
                    new_node.grandparent().color = 'red'
                    new_node = new_node.grandparent()
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.rotate_left(new_node)
                    new_node.parent.color = 'black'
                    new_node.grandparent().color = 'red'
                    self.rotate_right(new_node.grandparent())

            else:
                uncle = new_node.uncle()
                if uncle and uncle.color == 'red':
                    new_node.parent.color = 'black'
                    uncle.color = 'black'
                    new_node.grandparent().color = 'red'
                    new_node = new_node.grandparent()
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.rotate_right(new_node)
                    new_node.parent.color = 'black'
                    new_node.grandparent().color = 'red'
                    self.rotate_left(new_node.grandparent())
        self.root.color = 'black'


    # rotations are used when inserting and deleting to maintain balance
    def rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left

        if right_child.left is not None:
            right_child.left.parent = node

        right_child.parent = node.parent

        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

    # rotations are used when inserting and deleting to maintain balance
    def rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right

        if left_child.right is not None:
            left_child.right.parent = node

        left_child.parent = node.parent

        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child

        left_child.right = node
        node.parent = left_child

    # works exactly opposite of the insert function
    def delete(self, value):
        node_to_remove = self.search(value)

        if node_to_remove is None:
            return

        if node_to_remove.left is None and node_to_remove.right is None:
            self._replace_node(
                node_to_remove, node_to_remove.left or node_to_remove.right)

        else:
            successor = self._find_min(node_to_remove.right)
            node_to_remove.value = successor.value
            self._replace_node(successor, successor.right)

        self.delete_fix(node_to_remove)

    # checks after deletion that color integrity is maintained;
    # if not, performs the rotations necessary to correct
    def delete_fix(self, x):
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                sibling = x.sibling()
                if sibling.color == 'red':
                    sibling.color = 'black'
                    x.parent.color = 'red'
                    self.rotate_left(x.parent)
                    sibling = x.sibling()
                if (sibling.left is None or sibling.left.color == 'black') and sibling.right is None or sibling.right.color == 'black':
                    sibling.color = 'red'
                    x = x.parent

                else:
                    if sibling.right is None or sibling.right.color == 'black':
                        sibling.left.color = 'black'
                        sibling.color = 'red'
                        self.rotate_right(sibling)
                        sibling = x.sibling()
                    sibling.color = x.parent.color
                    x.parent.color = 'black'
                    if sibling.right:
                        sibling.right.color = 'black'
                    self.rotate_left(x.parent)
                    x = self.root

            else:
                sibling = x.sibling()
                if sibling.color == 'red':
                    sibling.color = 'black'
                    x.parent.color = 'red'
                    self.rotate_right(x.parent)
                    sibling = x.sibling()
                if (sibling.left is None or sibling.left.color == 'black') and (sibling.right is None or sibling.right.color == 'black'):
                    sibling.color = 'red'
                    x = x.parent
                else:
                    if sibling.left is None or sibling.left.color == 'black':
                        sibling.right.color = 'black'
                        sibling.color = 'red'
                        self.rotate_left(sibling)
                        sibling = x.sibling()
                    sibling.color = x.parent.color
                    x.parent.color = 'black'
                    if sibling.left:
                        sibling.left.color = 'black'
                    self.rotate_right(x.parent)
                    x = self.root
        x.color = 'black'

    # uses search to find node and update values
    def _replace_node(self, old_node, new_node):
        if old_node.parent is None:
            self.root = new_node
        else:
            if old_node == old_node.parent.left:
                old_node.parent.left = new_node
            else:
                old_node.parent.right = new_node
        if new_node is not None:
            new_node.parent = old_node.parent

    # function to find the smallest value in the tree (leftmost)
    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    # prints the nodes in order from least to greatest by looking
    # from leftmost to rightmost
    def _inorder_traversal(self, node):
        if node is not None:
            self._inorder_traversal(node.left)
            print(node.value, end=' ')
            self._inorder_traversal(node.right)

# builds list of prerequisites
def loadPrereqs(filename):
    prereqs = []
    try:
        with open(filename, mode= 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter= ',')
            for lines in reader:
                prereqs.append(lines[0])

        prereqs.append("")
        csvfile.close()
    except FileNotFoundError:
        print("File not found")

    return prereqs

# loads data from CSV file
def loadCSV(filename, prereqs, tree):
    try:
        with open(filename, mode = 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for lines in reader:
                # adjusts input length if there are not enough entries
                while len(lines) < 5:
                    lines.append("")
                # makes sure prerequisites exist, if not it skips the entry
                if lines[2] not in prereqs:
                    continue

                if lines[3] not in prereqs:
                    continue

                if lines[4] not in prereqs:
                    continue

                newCourse = Course(lines[0], lines[1], lines[2], lines[3], lines[4])
                tree.insert(lines[0], newCourse)

            print("Loaded Successfully")
            csvfile.close()
    except FileNotFoundError:
        print("File not found")


    return tree


# menu logic, display only
def menu():
    print('#' * 40)
    print("1. Load Data Structure")
    print("2. Print Course List")
    print("3. Print Course")
    print("4. Exit")
    print('#' * 40)
    print()

# switch case for menu selection
def switch_case(tree):
    choice = 0
    while choice != 4:
        menu()
        choice = int(input("Enter your choice: "))
        match choice:
            case 1:
                fileName = input("Please enter the file name: ")
                prereqs = loadPrereqs(f"{fileName}.csv")
                tree = loadCSV(f"{fileName}.csv", prereqs, tree)
            case 2:
                tree._inorder_traversal(tree.root)
                print()
                print()
            case 3:
                searchItem = input("Please enter the Course ID: ")
                result = tree.search(searchItem)
                if result:
                    Course.print_result(result.course)
                else:
                    print("No such course.")
            case 4:
                quit(0)