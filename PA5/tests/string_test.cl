class Main inherits IO {
    a : Int <- 222;
    b : Int <- 333;
    c : String <- "Hello World!";
    main() : Object {{
        temp(a, b, 10);
        out_string(c);
    }};
    temp(one : Int, two : Int, three : Int) : Object {
        out_int(one + two + three)
    };
};