import random

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
from block import Block


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
                # util.log(
                #     "Solution unfeasible. Collision between blocks {} and {}".format(
                #         block.name, block2.name
                #     )
                # )

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
    def calc_single_connection_length(connection):
        firstBlock = next((x for x in blocks if x.name == connection.first), Block.default())
        secondBlock = next((x for x in blocks if x.name == connection.second), Block.default())
        return math.dist(firstBlock.get_mid_point(), secondBlock.get_mid_point())
    sum = 0
    for connection in connections:
        sum += calc_single_connection_length(connection)
    return sum

def calc_obj_function(blocks, connections, alpha, beta):
    max_y = max([block.positionY + block.height for block in blocks])
    max_x = max([block.positionX + block.width for block in blocks])

    L = calc_connection_length(blocks, connections)
    A = max_y * max_x

    return alpha * A + beta * L

def calc_obj_function_ideal(blocks, connections, alpha, beta):
    A = 0
    for block in blocks:
        A += block.width * block.height
    L = 0

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
        operation = random.randint(0, 3)
        if operation == 0:
            candidate_tree = treemanip.swap_random_nodes(tree)
        if operation == 1:
            candidate_tree = treemanip.rotate_random_node(tree, blocks)
        if operation == 2:
            candidate_tree = treemanip.move_random_node(tree)
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

    print(connections);
    graphics.placement_visualisation("results.png", blocks, scale=0.1, fontscale=1.0)

    while True:
        block_names = [block.name for block in blocks]
        random.shuffle(block_names)

        binary_tree = binarytree.build(block_names)

        nb = place_blocks(binary_tree, blocks)

        if check_if_feasible(blocks):
            break
    # Parameters
    initTemp = 2000
    MaxOneTempIterations = 5
    alpha = 0.8
    beta = 0.2
    ##########################
    currentTempIterations = 0
    it = 0
    bestEval = 9999999999
    bestTree = binary_tree
    bestBlocks = blocks
    idealSolution = calc_obj_function_ideal(blocks, connections, alpha, beta)
    acceptableError = 0.2
    lookingForBestResult = True
    candidatesEvaluations = []
    bestEvaluations = []
    temperatuers = [initTemp]
    while lookingForBestResult:
        if currentTempIterations >= MaxOneTempIterations:
            it += 1
            currentTempIterations = 0
        addedCurrentBestEval = False
        candidateBlocks, candidateTree = find_random_possible_change(bestBlocks, bestTree)
        candidateEval = calc_obj_function(candidateBlocks, connections, alpha, beta)
        candidatesEvaluations.append((candidateEval - idealSolution)/idealSolution)
        if bestEval > candidateEval:
            bestEval, bestTree, bestBlocks = candidateEval, candidateTree, candidateBlocks
            currentTempIterations = 0
            it += 1
        else:
            diff = (bestEval - candidateEval) / idealSolution
            initTemp = (initTemp / (it + 1) ) 
            # #* abs(1-diff)
            # initTemp = initTemp * (1-abs(-diff))

            temperatuers.append(initTemp)
            rand = random.random()
            shouldAcceptWorseCandidate = rand < diff+initTemp

            if shouldAcceptWorseCandidate:
                bestEval, bestTree, bestBlocks = candidateEval, candidateTree, candidateBlocks
                currentTempIterations = 0
                it += 1
            else:
                currentTempIterations += 1
        bestEvaluations.append(bestEval)
        if bestEval <= idealSolution * (1 + acceptableError):
            lookingForBestResult = False

    plt.plot(range(0, len(candidatesEvaluations)), candidatesEvaluations)
    plt.xlabel("Nr iteracji");
    plt.ylabel("Wartość funkcji celu");
    plt.show()
    plt.plot(range(0, len(temperatuers)), temperatuers)
    plt.xlabel("Nr iteracji");
    plt.ylabel("Temperatura");
    plt.show()
    plt.plot(range(0, len(bestEvaluations)), bestEvaluations)
    plt.xlabel("Nr iteracji");
    plt.ylabel("Najniższa wartośc f.  celu");
    plt.show()
    save_to_file(bestBlocks, connections, bestTree)
    graphics.placement_visualisation("results_final.png", bestBlocks, scale=0.1, fontscale=1.0)
