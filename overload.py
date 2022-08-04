import inspect
from typing import Callable, Optional

table = dict()


def debug_message(message: str):
    print(f"[overload-debug]: {message}")


class Overload:
    __DEFAULT_HASH_TABLE = dict()

    def __init__(self, separate_hash_table: dict = None, debug: bool = False):
        self.func: Optional[Callable] = None
        self.hash_table = separate_hash_table \
            if separate_hash_table else table
        self.argspec_key_pattern = "{args}:{defaults}:{returns}"
        self.debug = debug if debug else False

    def get_function_hash(self, key):
        # Default hash function algo
        # You can customize hashing algorithm you want
        return abs(
            # Making hash with declaring key and wrapped function id
            # (its fully unique now, and it's ready for hash table)
            hash(
                key + str(id(self.func))
            )
        )

    def __call__(self, *args, **kwargs):
        """
        :param args: args[0] - wrapped func or method
        :param kwargs: empty!
        :return: Callable wrapper
        """
        self.func = args[0]

        # Definition case
        # Inspecting wrapped function for getting types annotations
        argspec: inspect.FullArgSpec = inspect.getfullargspec(self.func)

        # TODO:
        #   add default value support in cases
        #   when it was declared and func
        #   ---
        #   >>> @overload
        #   >>> def fetch(self, a: Optional[List] = None) -> List:
        #   >>>     return list()
        #   ---
        #   but not given at `fetch` call:
        #       fetch() > TypeError: TestArrays.fetch()
        #       missing 1 required positional argument: 'a'
        #   bug passed if we call fetch with all arguments
        #       fetch(None) > works
        #   ---
        #   try python3 trouble.py

        # Ccomon case
        # Declaring key for hash table (it's not unique yet)
        key = self.argspec_key_pattern.format(
            args=argspec.args,
            defaults=argspec.defaults,
            returns=argspec.annotations.get('return')
        )

        # Common case
        # Hash function algo
        function_hash_key = self.get_function_hash(key)

        # Definition case
        # Saving function in hash table for hash_function_key
        self.hash_table.update({
            function_hash_key: self.func
        })

        # Evaluation case
        # Return a wrapper that will return the
        # target function from the hash table
        def call_function_by_hash_table_key(*a, **kw):
            try:
                return self.hash_table[function_hash_key](*a, **kw)
            except KeyError as e:
                # Exception case when function_hash_key
                # was not found in hash table
                # In this case will be returns input wrapped func
                return self.func(*a, **kw)

        if self.debug:
            debug_message(f"hash table state: {self.hash_table}")

        return call_function_by_hash_table_key
