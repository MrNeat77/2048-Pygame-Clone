# 2048 Game

A personal project so I can learn about basic game development, python, pygame, OOP, and coming up with creative algoithms.

---
This is a *learning* opportunity, so of course there are best practices missed, and some of the methods implemented are not as efficient as other potential methods. I did this on purpose in order to stretch my ability and come up with a solution a *certain way*, and not use the "best" solution.

For example: the `move()` method in board.py takes a directional input, and uses **one** algorithm to iterate through the board multiple different ways, and uses a dictionary to turn the direction input into a set of instructions. It would have probably been "better" to just create a smaller unique algorithm for each direction instead of the big algorithm and dictionary system, however doing it this way allowed me to create an algorithm that is able to change based on sets of instructions.