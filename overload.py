import inspect
from functools import lru_cache
from typing import Callable, Optional

default_hash_table = dict()


class Overload:
    def __init__(self, separate_hash_table: dict = None):
        self.func: Optional[Callable] = None
        self.hash_table = separate_hash_table \
            if separate_hash_table else default_hash_table
        self.argspec_key_pattern = "{args}:{defaults}:{returns}"

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

        # DEFINITION CASE
        # Inspecting wrapped function for getting types annotations
        argspec: inspect.FullArgSpec = inspect.getfullargspec(self.func)

        # COMMON CASE
        # Declaring key for hash table (it's not unique yet)
        key = self.argspec_key_pattern.format(
            args=argspec.args,
            defaults=argspec.defaults,
            returns=argspec.annotations.get('return')
        )

        # COMMON CASE
        # Hash function algo
        function_hash_key = self.get_function_hash(key)

        # DEFINITION CASE
        # Saving function in hash table for hash_function_key
        self.hash_table.update({
            function_hash_key: self.func
        })

        # EVALUATION CASE
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

        return call_function_by_hash_table_key
