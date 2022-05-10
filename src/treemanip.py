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

        log("Moving {} to {}".format(node_1.value, new_parent.value))

        # Remove node from old parent
        parent_1 = binarytree.get_parent(new_tree, node_1)
        remove_child(parent_1, node_1)

        insert_child_random(new_parent, node_1)

        return new_tree


def rotate_random_node(tree, blocks):
    new_tree = tree.clone()
    node = get_random_node(new_tree)

    log("Rotating block {}".format(node.value))

    block = get_block_by_name(blocks, node.value)
    block.rotate()  # type:ignore

    return new_tree


# def swap_random_nodes(tree):
#     new_tree = tree.clone()
#     while True:
#         node_1 = get_random_node(new_tree)
#         node_2 = get_random_node(new_tree)

#         if node_1 == node_2:
#             continue

#         if node_1 == new_tree or node_2 == new_tree:
#             # We need to rebuild tree
#             # do nothing for now
#             return new_tree

#         log("Swapping {} and {}".format(node_1.value, node_2.value))

#         parent_1 = binarytree.get_parent(new_tree, node_1)
#         parent_2 = binarytree.get_parent(new_tree, node_2)

#         if parent_1.left == node_1:
#             parent_1.left = node_2
#         else:
#             parent_1.right = node_2

#         if parent_2.left == node_2:
#             parent_2.left = node_1
#         else:
#             parent_2.right = node_1

#         return new_tree
