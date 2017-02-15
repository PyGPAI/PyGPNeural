# Input Utilities

A few useful classes for handling input.

Handling input should be done with specific libraries

## Global

Some python libraries send the python input class to a dll, where some data may be lost, like 'self'. To solve this, a few variables had to be defined globally. Unfortunately, this means either only one input source of the same type can be used, or each input must be prefaced by a unique identifier for its input source.

