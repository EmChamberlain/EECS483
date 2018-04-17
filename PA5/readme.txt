Matthew Chamberlain, mattcham, 40136524

python2.7 main.py <in.cl-type> (on CAEN)
main.py takes data from a file specified on the command line and outputs a compiled Cool assembly program to <in.cl>-asm.

Required Files:
AST.py is my Object Oriented implementation of the AST nodes
Utilities.py is a class that I use for keeping track of Utility functions

I used the video guides posted https://dijkstra.eecs.umich.edu/eecs483/pa5.php as a starting point.

test1.cl:
This test goes over some basics like arithmetic, dispatch, attribute assignment, inheritance, overriding, etc. The important part of this test (and the part that really helped me) was the weird case checks. First I checked for proper scoping in case statements for both let bindings and attributes. Then I checked for if the symbol table was contaminated within further function calls. I found a bug here where I was allowing the symbol table to stay changed within function arguments which shouldn't happen. I then checked other possible venues of contamination of the symbol table but couldn't find any. I then checked whether nested cases work properly and found a bug here where cases were overriding the previous case because of poor symbol table management.

test2.cl:
This test goes over the same basic stuff like in test1. This test is focuses on testing lets. The first thing I did was test for properly scoped nested lets which lead me to a large change in how I handle let bindings which I will detail below. I then checked to make sure that non-initialized values in the let behaved correctly. I then checked if assignment was working correctly in the let and I found yet another bug with how I was handling the symbol table. I was not properly maintaining the scope of the symbol table so a let with the same bindings as before could interact with the wrong data structures.

test3.cl:
This test goes over the same basics as before. This focuses on some more strange expressions than normal. I tested dispatching on a brand new class which lead me to a bug where I was not maintaining stack discipline. I tested repeated string concatenation with itself. I tested creating a new class of itself then dispatching on it which was then passed as a parameter. I then tested dispatching on new expressions. Finally, I tested statically dispatching on a new expression. This lead my down a rabbit hole of bugs but eventually I found out that I was not properly handling the creation of new objects. Originally, if there was no initializer for an attribute, I would write 0 to it so that I would know if it was void or not. This sort of behaviour does not play well if that attribute is an internal class. This bug was so hard to track down because I had two different places where I was handling nulling out attributes and only one of them was buggy. I fixed this by unifying them into one place.

test4.cl:
This was the first test I used. It still tests the basics. I started it off with some stress tests on arithmetic. I generated massively nested expressions and found out that I had to up the python recursion limit to actually be able to run it. Theoretically I am still vulnerable to running out of stack space though. This massive arithmetic also tested integer behaviour. I then start to test all of the internals in a variety of ways. Checking for type_name returning a string object instead of a raw string. Check that in_string and in_int work properly. Checking that length and concat work properly. I initially had a bug where concat was not returning a String object but I fixed that. Substr gave me a bit of a hard time because I was trying to just use r0, r1, and r2 but I eventually used a 4th register to implement it. Then finally testing that abort works.



Implementation of the compiler:
Initially I followed the video guides to get an intuition for what I needed to accomplish. The video guides where gave me a great head start and set me up with some of the important features of my compiler. I will talk about each section chronologically.

    Start:
    I just hard-coded the start label in like the video guide.

    Serialization:
    I was able to re-use my AST implementation from PA4 mostly unchanged. Each different piece of Cool syntax had a class made for them. Classes, attributes, formals, expressions, etc. Each class can create an object that stores everything I might need to know about that object taken directly from the input. It was relatively easy after that to build some helper functions to help me read in the class_map and the implementation_map; I did not use either the parent_map nor the AAST.

    Vtables:
    For vtables, I used the guide's name mangling to make sure there were no problems there. My vtables are laid out first with a string constant label used for the internal function type_name(). Then I have the constructor. Then I have all of the methods that are in the implementation table after that.

    Globals:
    I set up a globals section for all of the string constants I was going to use throughout the program. This contained things like the empty string, error strings, type_name strings, and other string constants the programmer declared. I built up this list of globals during the reading in of the implementation map and my AST classes where able to communicate with my main through my Utilities file.

    Stack Discipline:
    I think that now is a good time to talk about my stack discipline. For me, the caller was responsible for things in this order: push fp, push self, change self if needed, call callee, pop self, pop fp. The callee was responsible for: updating the fp so that we are on unused stack space, push ra, executing the called function, save return value to my accumulator (r1), pop ra, and then returning. This setup allowed me to set up some helper functions so that it would be hard to not conform to the stack discipline. I made some helper functions so that the calling of functions was done automatically according to this discipline. The hard part about this discipline is the callee. When I talk about my method implementation you should have a better understanding.

    Constructors:
    I had standard constructors just like the guide. I had to add some space for the type_name but that was it. I first alloced some space then I began filling it first with internal attributes like the vtable pointer and the object size. Then I started putting in declared attributes. This consisted of calling the correct constructor and then filling the returned data structure or primitive. Then I simply returned the pointer to the alloced space.

    Methods:
    I next have all of my hard-coded internal methods. I hard-coded them so you can see what I did if you look at my main.py but it is very close to the reference compiler. I then had all of my declared methods. I first made sure that none of the internal methods got overriden and then setup a label and the callee initialization. I filled my symbol table as well as pushed my formals onto the stack. I did not push them in reverse order so in dispatch code generation I had to account for that. The body of the method is then the code generation of the body expression.

    Code generation:
    My code generation was relatively straight forward. All of the expression in my AST.py classes inherited from an overall Expression class. This allowed my to make a method for each one that independently handled code generation. If an expression needed to evaluate another expression, it simply called that expression's cgen method. This ended in a few things like string constants that would return a string, identifiers that would look themselves up in the symbol table, etc. This is where a bulk of my time was spent because of all of the different expressions.

    Dispatch:
    I handled dispatch by first finding my method in the implementation_map. Then I called cgen on all of the arguments and pushed them onto the stack directly after the cgen returned. I then got the correct vtable in an appropriate manner (static statically, dynamic dynamically). I then called cgen on the recieving object if I needed to. I then called the function in question. Once the call was done I popped all of my arguments off the stack and returned.






























