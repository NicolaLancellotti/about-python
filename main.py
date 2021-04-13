from main_module import Language
from main_module import Builtins
from main_module import Classes
from main_module import StandardLibrary
from main_module import Patterns

if __name__ == "__main__":
    Language.expressions()
    Language.statements()
    Language.functions()
    Language.iterators_generators()
    Language.corutines()
    Language.scope()
    Language.packages()

    Builtins.type_strings()
    Builtins.type_bytes()
    Builtins.type_tuples()
    Builtins.type_lists()
    Builtins.type_dictionaries()
    Builtins.type_sets()

    Classes.run()

    StandardLibrary.type_hints()
    StandardLibrary.arguments()
    StandardLibrary.functional_programming()
    StandardLibrary.enumerations()
    StandardLibrary.data_classes()
    StandardLibrary.abstract_classes()
    StandardLibrary.regex()

    Patterns.proxy()
    Patterns.frozen_classes()
