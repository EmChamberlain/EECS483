Matthew Chamberlain, mattcham, 40136524

python2.7 main.py <in.cl-lex> (on CAEN)
main.py takes data from a file specified on the command line and outputs a complete AST to <in.cl>-ast.

Required Files:
lex.py is the PLY lexical analyzer generator taken from http://www.dabeaz.com/ply/.
yacc.py is the PLY parser generator taken from http://www.dabeaz.com/ply/.

I used the video guide https://www.youtube.com/watch?v=kearNtiYWr8 as a starting guide.

good.cl is a large test file that should have no syntax errors. It tests many cases, but the more important ones are precedence, associativity, dispatch of all kinds, string literal whitespace preservation, blocks, multiple classes, etc. I also used my rosetta.cl as a secondary test to make sure that I was getting the same output as the reference parser on a larger "real" Cool program.

bad.cl is a test file that tests a bunch of different syntax errors. I built the file as I was debugging but started the file with a few valid lines, so I knew my problem wasn't with the block or something else. bad.cl tests comma placement in all types of dispatch as well as methods.

Initially I followed the video guide to get a jump start on understanding Yacc from PLY. The precedence setup I used came straight from the Cool documentation except for the IN token from the let expression. It makes sense that IN would be left associative, but I am not positive it should have less strict binding than LARROW. I used a similar list representation for all lists that appear in Cool syntax. They differ slightly from each other because of nuances in Cool like delimiters being commas or semicolons, allowing empty lists, or not allowing trailing delimiters. I liked how the method for outputting lists from the video guide, so I used that as a base for outputting lists. I used a list_str method that would take a list of elements and a method that is supposed to be used to print out those elements. My expression output is a relatively long elif chain, but I don't really think there is a more readable way to do what needs to be done.
