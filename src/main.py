import files
import binarytree


if __name__ == "__main__":

    try:
        (blocks, connections) = files.load_file()
    except:
        exit()

    block_names = [block.name for block in blocks]

    print(block_names)

    binary_tree = binarytree.build(block_names)
    print('Binary tree from list :\n',
      binary_tree)
 

    # for block in blocks:
    #     print(block.toJSON())