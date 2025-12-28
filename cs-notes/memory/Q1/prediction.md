# Prediction (before probing)

My current belief (likely incomplete or wrong):

- A program does not directly access memory.
- It likely talks to some memory-managing component.
- This component checks the address requested.
- It then fetches the data from memory and returns it to the program.

I imagine:
- Memory is indexed in some form.
- Accessing memory means reading bits from specific locations.
- If multiple programs access memory, there must be some queue or ordering.

Assumptions I am making:
- There is a central controller or "memory manager".
- Programs actively request data and wait for a response.