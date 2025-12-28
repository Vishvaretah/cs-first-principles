#!/usr/bin/env python3
"""
Demonstration: access memory-related details in Python and explain what happens step-by-step.
This script is safe (no arbitrary memory reads) and uses Python APIs: id(), sys.getsizeof(),
memoryview, ctypes.from_buffer to show buffer addresses for objects that expose the buffer protocol.

Run with: python cs-probes/memory/Q1.py
"""
import sys
import ctypes


def print_header(title):
    print('\n' + '=' * 60)
    print(title)
    print('=' * 60 + '\n')


def integers_and_ids():
    print_header('1) Integers and object identity (id)')
    a = 1000
    b = a
    print(f"a = {a}, b = {b}")
    print(f"id(a) = {id(a):#x}")
    print(f"id(b) = {id(b):#x}  (same as a because b references the same integer object)")
    print('\nNow change b to a new integer value:')
    b = 1001
    print(f"a = {a} (unchanged)")
    print(f"b = {b}")
    print(f"id(a) = {id(a):#x}")
    print(f"id(b) = {id(b):#x}  (different; integers are immutable, assignment binds name to a new int)")


def lists_and_mutability():
    print_header('2) Lists, element identity, and mutability')
    L = [1, 2, 3]
    print(f"L = {L}")
    print(f"id(L) = {id(L):#x}")
    print(f"id(L[0]) = {id(L[0]):#x} (small integers may be interned but are still separate objects)")

    x = L[0]
    print('\nBind x = L[0] (x references the integer object that L[0] references)')
    print(f"x = {x}, id(x) = {id(x):#x}")

    print('\nModify L[0] = 99 (this changes the list slot to reference a different integer)')
    L[0] = 99
    print(f"L = {L}")
    print(f"x = {x} (unchanged because integers are immutable and x still references the old object)")

    print('\nNow show a mutable element inside a list:')
    M = [[1], [2]]
    print(f"M = {M}")
    print(f"id(M) = {id(M):#x}")
    print(f"id(M[0]) = {id(M[0]):#x} (a sublist object)")

    y = M[0]
    print('\nBind y = M[0] (y and M[0] reference the same inner list)')
    print(f"y = {y}, id(y) = {id(y):#x}")

    print('\nMutate the inner list via y[0] = 9 (this mutates the single object referenced by both y and M[0])')
    y[0] = 9
    print(f"M = {M}")
    print(f"y = {y} (change visible through both references because the object is mutable)")


def bytearray_and_buffer():
    print_header('3) bytearray, memoryview, buffer address, and direct byte mutation')
    ba = bytearray(b'hello')
    print(f"Initial bytearray: {ba}")
    print(f"id(ba) = {id(ba):#x}")
    print(f"sys.getsizeof(ba) = {sys.getsizeof(ba)} bytes (object overhead + buffer)")

    mv = memoryview(ba)
    print(f"memoryview(ba) gives a view into the same buffer with length = {mv.nbytes}")
    print("Bytes (as list):", list(mv))

    # Show the address of the underlying buffer for objects that expose the buffer protocol.
    try:
        buf_addr = ctypes.addressof(ctypes.c_char.from_buffer(ba))
        print(f"Address of the bytearray buffer: {buf_addr:#x}")
    except (TypeError, BufferError):
        print("Could not obtain buffer address for this object on this Python build.")

    print('\nModify the second byte: ba[1] = ord(\'a\')')
    ba[1] = ord('a')
    print(f"Modified bytearray: {ba}")
    print("This shows mutation in-place: the bytearray exposes a writable buffer, so the same memory changed.")


def refcounts_demo():
    print_header('4) Reference counts (sys.getrefcount)')
    import sys as _sys
    obj = []
    print(f"Create an empty list object obj = [] with id = {id(obj):#x}")
    rc1 = _sys.getrefcount(obj)
    print(f"sys.getrefcount(obj) = {rc1} (note: passing obj to getrefcount temporarily increments the count by 1)")

    alias = obj
    rc2 = _sys.getrefcount(obj)
    print(f"After alias = obj, sys.getrefcount(obj) = {rc2} (one more reference from alias)")

    del alias
    rc3 = _sys.getrefcount(obj)
    print(f"After del alias, sys.getrefcount(obj) = {rc3} (reference count goes down)")

    print('\nReference counts reflect how many Python-level references point to the object. Garbage collection frees objects when counts drop to zero (plus cyclic GC for cycles).')


def main():
    print('Python memory access & behavior demonstration — step by step')
    integers_and_ids()
    lists_and_mutability()
    bytearray_and_buffer()
    refcounts_demo()
    print('\nDone.')


if __name__ == '__main__':
    main()