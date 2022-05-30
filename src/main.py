import random
from time import sleep

import numpy
import numpy as np

import files
import graphics
import binarytree
import treemanip
import util
import math
import matplotlib.pyplot as plt

# TODO
# wyrzarzanie
# obliczanie pola
# definicja polaczen?(środki)
# 1. Znajdź nowe randomowe położenie
# 2. Sprawdź, czy lepsze
# 3. Jeśli jest lepsze, zastąp starsze rozwiązanie, jeśli nie, to jest losowa szansa że przyjmujemy gorsze rozwiązanie (zależna od temperatury)
# 3. Zmniejsz temperaturę
# Goto 1

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


def visit_node(bloks, node, parent, is_left_child):
    if node is None:
        return

    parent_block = treemanip.get_block_by_name(bloks, parent.value)

    if is_left_child:
        posX = parent_block.positionX + parent_block.width  # type:ignore
        posY = parent_block.positionY  # type:ignore

        set_block_position(bloks, node.value, posX, posY)
    else:
        posX = parent_block.positionX  # type:ignore
        posY = parent_block.positionY + parent_block.height  # type:ignore

        set_block_position(bloks, node.value, posX, posY)

    visit_node(bloks, node.left, node, True)
    visit_node(bloks, node.right, node, False)


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


def save_to_file(blocks, connections, tree):
    block_string = ""
    for block in blocks:
        block_string += block.toJSON() + ","

    # Remove trailing comma
    block_string = block_string[:-1]

    output_str = '{{\n"blocks":[{}],\n "connections":{},\n "tree":{}\n}}'.format(
        block_string, connections, str(tree.values).replace("'", '"')
    )

    with open("result.json", "w") as file:
        file.write(output_str)


def find_random_possible_change(blocks, tree):
    while True:
        operation = random.randint(0, 1)
        if operation == 0:
            candidate_tree = treemanip.swap_random_nodes(tree)
        else:
            candidate_tree = treemanip.move_random_node(tree)

        candidate_blocks = place_blocks(candidate_tree, blocks)

        if check_if_feasible(blocks):
            return candidate_blocks, candidate_tree


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

    initTemp = 1000
    it = 0
    bestEval = graphics.get_eval(blocks)
    bestTree = binary_tree
    bestBlocks = blocks
    idealSolution = graphics.get_ideal_eval(blocks)
    acceptableError = 0.1
    lookingForBestResult = True
    candidatesEvaluations = []
    temperatuers = [initTemp]
    while lookingForBestResult:
        it += 1
        candidateBlocks, candidateTree = find_random_possible_change(bestBlocks, bestTree)
        candidateEval = graphics.get_eval(candidateBlocks)
        candidatesEvaluations.append(candidateEval-idealSolution)
        if bestEval > candidateEval:
            bestEval, bestTree, bestBlocks = candidateEval, candidateTree, candidateBlocks
        else:
            diff = (bestEval - candidateEval)/100000
            temp = initTemp/(it + 1)
            temperatuers.append(temp)
            rand = random.random()
            print(diff, temp)
            exp = np.exp(-diff/temp)
            print("rand \t exp \t diff\n", rand, exp, diff)
            shouldAcceptWorseCandidate = rand < exp
            if shouldAcceptWorseCandidate:
                bestEval, bestTree, bestBlocks = candidateEval, candidateTree, candidateBlocks
        if bestEval <= idealSolution * (1 + acceptableError):
            break



    plt.plot(range(0, len(candidatesEvaluations)), candidatesEvaluations)
    plt.show()
    plt.plot(range(0, len(temperatuers)), temperatuers)
    plt.show()
    save_to_file(bestBlocks, connections, bestTree)
    graphics.placement_visualisation("results_final.png", bestBlocks, scale=0.1, fontscale=1.0)

