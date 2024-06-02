## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Working](#working)
- [Not working](#notworking)
- [Conclusion](#conclusion)

## Overview
This is my implementation of the Quack language compiler for CS 461. The main files are:

    - compiler.py: This the main file for the compiler process. It loads the grammar, test program, and parses both of them. I tried to add more robust tracking of exceptions to diagnose issues with compilation more accurately.

    - QuackTransformer.py: This is the transformer class for lark. Based on the grammar file, it interprets the rules which end up determining the structure when the AST is converted into a concrete syntax tree.

    - AST.py: This file lays out the classes for each node in our concrete syntax tree. There is a base class of ASTNode, and all of the other nodes inherit from this class. It also includes a graph function that produces a graph of the concrete syntax tree.

    - QuackChecker.py: This is my basic type checker/handler class. It takes the concrete syntax tree as a member, and traverses it. QuackChecker can check for basic type mismatching on
    operators, and also check to make sure variables are initialized before use.

    -quack.sh: Bash script that runs the compilation process from start to finish.
    
    -quack_mass.sh: Bash script that runs the compilation process from start to finish on every quack file in a directory.



## Installation
This repo includes a script titled "quack.sh" for easy compilation. To run, use:

```console
./quack.sh "file.qk"
```

There is a directory titled "test_progs" which contains a sample of working Quack programs. Some of the provided test programs will result in an exception intentionally. This demonstrates the small amount of type checking and error handling that I have included. You can also run:

```console
./quack_mass.sh "directory_name"
```

in order to compile every quack program in a directory.

## Working

Here is a list of what I have been able to implement so far:

- [X] Basic variables
- [X] If/Elif/Else
- [X] While Loops
- [X] Basic type checking
- [X] Return statements
- [X] Assignment statements (initialzes and updates to variables)
- [X] Basic Type Checking


## Not Working

I was not able to get far enough for classes and methods. I was advised to take on type checking instead, so I have a very stripped down basic type checker running currently.

- [ ] Class/Methods
- [ ] Real Type Checking


## Overview

Overall this project was very intersting, and I have learned so much in this course over the term. I think that the only other class I learned so much in would have to be Operating Systems. I am feeling pretty good about what I have achieved so far, and it is incredible to be able to run our own code with a custom language all the down into the Tiny Virtual Machine. This course has definitely reignited some interest in doing low level programming, especially after writing so much python and javascript lately.