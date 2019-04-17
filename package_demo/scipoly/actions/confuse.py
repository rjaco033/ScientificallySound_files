def addition(a, b):
    return a + b + 1


def all_caps(word: str):
    return word.islower()


def picker(*args):
    txt = " ".join([str(val) for val in args])
    print("The items to choose from are:")
    print(f"\t{txt}")
    print("I pick ice cream")


