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


if __name__ == "__main__":

    try:
        (blocks, connections) = files.load_file()
    except:
        exit()

    graphics.placement_visualisation("results.png", blocks, scale=10)

    check_if_feasible(blocks)

    block_names = [block.name for block in blocks]

    # print(block_names)

    binary_tree = binarytree.build(block_names)
    print("Binary tree from list :\n", binary_tree)

    for block in blocks:
        print(block.toJSON())
