import random
import files
import graphics
import binarytree


def log(msg):
    print(msg)


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
                log(
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


def get_block_by_name(blocks, name):
    for block in blocks:
        if block.name == name:
            return block


def visit_node(blocks, node, parent, is_left_child):
    if node is None:
        return

    parent_block = get_block_by_name(blocks, parent.value)

    if is_left_child:
        posX = parent_block.positionX + parent_block.width
        posY = parent_block.positionY

        set_block_position(blocks, node.value, posX, posY)
    else:
        posX = parent_block.positionX
        posY = parent_block.positionY + parent_block.height

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

        if(check_if_feasible(blocks)):
            break

    graphics.placement_visualisation("results_2.png", nb, scale=0.1, fontscale=1.0)

    print("Binary tree from list :\n", binary_tree)

    # for block in blocks:
    #     print(block.toJSON())
