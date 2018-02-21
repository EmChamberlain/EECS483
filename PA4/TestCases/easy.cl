class Main {
    x : Int <- 0;
    y : Int;
    main() : Object {
        x + y
    };
};
class Main1 inherits Main {
    method() : Object {
        x*2
    };
    method1() : String {
        "Hello World"
    };
    method2() : Bool {
        false
    };
};