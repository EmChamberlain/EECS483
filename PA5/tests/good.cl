class Main inherits IO {
    x : Int <- 0;
    y : Int;
    main() : Int {
    {
        y <- 7;
        10 + x + y;
        1 / 2 + x - y;
        x + y;
    }
    };
    method1() : Int {
        main() + 6
    };
};

class Main1 {
    x : Int <- 0;
    y : Int;
    main() : Int {
    {
        y <- 7;
        10 + x + y;
        1 / 2 + x - y;
        x + y;
    }
    };
    method1() : Int {
        main() + 6
    };
};

class MainInh inherits Main {
    eleven() : Int {
        11
    };
};