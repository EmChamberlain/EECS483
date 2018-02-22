class Main {
    x : Int <- y + 1;
    y : Int <- x + 1;
    w : Int;
    z : Int;
    main() : Object { {
        x + y;
        w + z;
        x + z;
        let var : Int <- 5 in
            var + y;
        x + y / 2 * 12 - w + 4;
    }};
};

class Alt1 {
    method1() : Int { 
        15/12
    };
    method2() : Int {
        8 + 4
    };
    method3() : Int {
        method1() + method2()
    };
};

class Alt2 inherits Alt1 {
    cl : Alt1;
    two_method_1() : Int {
        method1() + cl.method2()
    };
};
