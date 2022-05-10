import random
from time import sleep
import files
import graphics
import binarytree
import treemanip
import util


def check_if_feasible(blocks):
    # check if blocks don't collide
    for block in blocks:
        for block2 in blocks:
            if block == block2:
                continue

            if (
                block.positionX < block2.positionX + block2.width
                and block.positionX + block.width > block2.positionX
                and block.positionY < block2.positionY + block2.height
                and block.height + block.positionY > block2.positionY
            ):
                util.log(
                    "Solution unfeasible. Collision between blocks {} and {}".format(
                        block.name, block2.name
                    )
                )

                return False

    return True


def set_block_position(blocks, name, positionX, positionY):
    for block in blocks:
        if block.name == name:
            block.positionX = positionX
            block.positionY = positionY


def visit_node(blocks, node, parent, is_left_child):
    if node is None:
        return

    parent_block = treemanip.get_block_by_name(blocks, parent.value)

    if is_left_child:
        posX = parent_block.positionX + parent_block.width  # type:ignore
        posY = parent_block.positionY  # type:ignore

        set_block_position(blocks, node.value, posX, posY)
    else:
        posX = parent_block.positionX  # type:ignore
        posY = parent_block.positionY + parent_block.height  # type:ignore

        set_block_position(blocks, node.value, posX, posY)

    visit_node(blocks, node.left, node, True)
    visit_node(blocks, node.right, node, False)


def place_blocks(tree_root, blocks):
    new_blocks = blocks.copy()

    r_name = tree_root.value
    set_block_position(new_blocks, r_name, 0, 0)

    visit_node(blocks, tree_root.left, tree_root, True)
    visit_node(blocks, tree_root.right, tree_root, False)

    return new_blocks


def calc_connection_length(blocks, connections):
    # TODO: implement connection length
    return 0.0


def calc_obj_function(blocks, connections, alpha, beta):
    max_y = max([block.positionY + block.height for block in blocks])
    max_x = max([block.positionX + block.width for block in blocks])

    L = calc_connection_length(blocks, connections)
    A = max_y * max_x

    return alpha * A + beta * L


if __name__ == "__main__":

    try:
        (blocks, connections) = files.load_file()
    except:
        exit()

    graphics.placement_visualisation("results.png", blocks, scale=0.1, fontscale=1.0)

    while True:
        block_names = [block.name for block in blocks]
        random.shuffle(block_names)

        binary_tree = binarytree.build(block_names)

        nb = place_blocks(binary_tree, blocks)

        if check_if_feasible(blocks):
            break

    graphics.placement_visualisation("results_2.png", nb, scale=0.1, fontscale=1.0)

    print("Binary tree from list :\n", binary_tree)

    print("Obj function val: ", calc_obj_function(nb, connections, 1.0, 0.0))

    new_tree = treemanip.rotate_random_node(binary_tree, blocks)
    nbr = place_blocks(new_tree, blocks)

    graphics.placement_visualisation("results_r.png", nbr, scale=0.1, fontscale=1.0)

    # while True:
    #     binary_tree = treemanip.move_random_node(binary_tree)
    #     print(binary_tree)
    #     sleep(1)

    # for block in blocks:
    #     print(block.toJSON())
