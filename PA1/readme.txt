Matthew Chamberlain, mattcham, 40136524

testcase.list contains 500 english words taken from https://github.com/dwyl/english-words

python rosetta.py (on CAEN)
rosetta.py takes data from stdin and outputs to stdout

python rosetta.cl (on CAEN)
rosetta.cl takes data from stdin and outputs to stdout

Since I am very comfortable with python I decided to do the python implementation first. I attempted to use nothing but lists in preparation for having to make my own data structures in my cool implementation. Therefore, I ended up storing the edges of the graph as a list of tuples of strings. In my python implementation, I was able to use many of the convenience aspects of python to get it done and working perfectly in very little time. There is only one thing I know is bad and that is the sort every time I insert into S. Since I already had an insertion sort implementation written for me in cool I new I didn't need to worry about writing it out in python. My overall goal with the python implementation was to make an outline for what I needed to do in cool. I did not want to do too many syntactically crazy things in python because it would only make my life harder later

This was my first program in cool so I had to get a hang of the syntax. I essentially just attempted to port my python version over line by line with some exceptions like the aforementioned insertion sort as well as having to implement a linked list that held tuples of strings as well as had some other functions I would need. There were two main "hacky" things I did in the cool version. The major one was that I just implemented a list of tuples of strings and when I only needed a list of strings I simply set the second in the tuple to the empty string. Second, I mixed and matched the functions in charge of changing the list. By that I mean the in my main function, I was editing the lists manually instead of calling functions to do it.

The cool implementation was definitely harder not just because of the different syntax but because of having to implement so much of the overhead that python just offers naturally. I picked up cool relatively fast and definitely learned more about it than I thought I could.

