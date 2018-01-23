Matthew Chamberlain, mattcham, 40136524

python main.py <in.cl> (on CAEN)
main.py takes data from a file specified on the command line and outputs to <in.cl>-lex

lex.py is the PLY lexical analyzer generator taken from http://www.dabeaz.com/ply/
I used the PLY documentation as starter code.


good.cl is a series of difficult to lex lines. It generally goes over what I was having trouble with when I couldn't pass a test on the auto grader. It goes over things like escaped strings, upper and lower case keyword handling, proper arithmetic parsing, '\0' in strings and a few other random tests.

bad.cl is a EOF error. I could have chosen either multi-line comment EOF or string EOF to submit but you can't test more than one EOF error per file. I chose a string EOF and fixing the bug I had relating to the string EOF allowed me to easily fix my multi-line comment EOF.

I setup a list of tokens according to the PLY documentation. I added all of the tokens in the assignment instructions as well as added tokens for single-line comments and multi-line comments. I setup basic regex to lex simple things like parenthesis and single-line comments but I used PLY's function method to lex more complex things like types, identifiers, and keywords. While basic searches online made it seem like it was possible to do strings and multi-line comments entirely through regex, I decided to use PLY's conditional lexing system to allow me to easily lex those. They both work similarly. I setup a new state in PLY for the comment/string. I then enter that state when I see the beginning of a new lexeme. I stay in that state until I see the end of the lexeme and then return back to PLY's INITIAL state to continue lexing the input. The trick to multi-line comments is that they might be nested so I needed to keep track of the level of nest that I was at to know if I was done with the lexeme. At the end of lexing, I write everything to the file except for the comments. In theory, I could also keep that information possibly for documentation purposes but that is not part of the assignment.

