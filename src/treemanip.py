import random
import binarytree
from util import log


def get_block_by_name(blocks, name):
    for block in blocks:
        if block.name == name:
            return block


def get_random_node(tree):
    nodes = tree.preorder
    return random.choice(nodes)


# I couldn't think of a better name lol
def get_random_node_with_free_place(tree):
    nodes = tree.preorder
    while True:
        node = random.choice(nodes)
        if node.left is None or node.right is None:
            return node


# checks if node_1 is an ancestor to node_2
def is_ancestor(root, node_1, node_2):
    node = node_2
    while True:
        parent = binarytree.get_parent(root, node)
        if parent == node_1:
            return True

        # we reached root without visiting node_1, so it can't be ancestor od node_2
        if parent == None:
            return False

        node = parent


def remove_child(parent, child):
    if parent.left == child:
        parent.left = None
    else:
        parent.right = None


def insert_child_random(parent, child):
    choice = random.randint(0, 1)

    # left is our first choice, assign to right if left is taken
    if choice == 1:
        if parent.left is None:
            parent.left = child
        else:
            parent.right = child
    # right is first choice in this case
    else:
        if parent.right is None:
            parent.right = child
        else:
            parent.left = child


def move_random_node(tree):
    new_tree = tree.clone()
    while True:
        node_1 = get_random_node(new_tree)
        new_parent = get_random_node_with_free_place(new_tree)

        # choose again when we get the same node twice
        if (node_1 == new_parent) or is_ancestor(new_tree, node_1, new_parent):
            continue

        # log("Moving {} to {}".format(node_1.value, new_parent.value))

        # Remove node from old parent
        parent_1 = binarytree.get_parent(new_tree, node_1)
        remove_child(parent_1, node_1)

        insert_child_random(new_parent, node_1)

        return new_tree


def rotate_random_node(tree, blocks):
    new_tree = tree.clone()
    blocks = list(blocks)
    node = get_random_node(new_tree)

    # log("Rotating block {}".format(node.value))

    block = get_block_by_name(blocks, node.value)
    block.rotate()  # type:ignore

    return new_tree, blocks


def swap_nodes_related(root, node_1, node_2, parent_1, parent_2):
    remove_child(parent_2, node_2)
    remove_child(parent_1, node_1)

    insert_child_random(parent_1, node_2)
    node = get_random_node_with_free_place(node_2)
    insert_child_random(node, node_1)

    return root

def swap_nodes_root(root, child):
    # just swap two nodes leaving their children in place
    # we're changing root so we need to build a new tree
    values = root.values

    for i in range(0, len(values)):
        if values[i] == child.value:
            values[i] = root.value
            
    values[0] = child.value

    new_tree = binarytree.build(values)
    return new_tree


def swap_unrelated(parent_1, parent_2, child_1, child_2):
    if parent_1.left == child_1:
        parent_1.left = child_2
    else:
        parent_1.right = child_2

    if parent_2.left == child_2:
        parent_2.left = child_1
    else:
        parent_2.right = child_1

def get_two_random_nodes(tree):
    while True:
        node_1 = get_random_node(tree)
        node_2 = get_random_node(tree)

        # choose randomly again if we selected the same node twice
        if node_1 == node_2:
            continue

        return (node_1, node_2)

def swap_random_nodes(tree):
    new_tree = tree.clone()
    (node_1, node_2) = get_two_random_nodes(new_tree)

    parent_1 = binarytree.get_parent(new_tree, node_1)
    parent_2 = binarytree.get_parent(new_tree, node_2)

    # log("Swapping {} and {}".format(node_1.value, node_2.value))

    # Handle case where one of nodes is the root
    if parent_1 is None:
        return swap_nodes_root(node_1, node_2)
    if parent_2 is None:
        return swap_nodes_root(node_2, node_1)

    if is_ancestor(new_tree, node_1, node_2):
        return swap_nodes_related(new_tree, node_1, node_2, parent_1, parent_2)
    if is_ancestor(new_tree, node_2, node_1):
        return swap_nodes_related(new_tree, node_2, node_1, parent_2, parent_1)

    # Nodes are not related, just swap pointers
    swap_unrelated(parent_1, parent_2, node_1, node_2)

    return new_tree
