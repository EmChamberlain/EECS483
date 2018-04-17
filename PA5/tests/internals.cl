class Main inherits IO {
    a : A <- new A;
    b : B <- new B;
    c : C <- new C;
    v : C;
    higher : Int <- 10;
    lower : Int <- 5;
    eq : Int <- 5;
    i : Int <- 0;
    instr : String;
    inint : Int;
    hello : String <- "Hello World!";
    main() : Object {
        {
            out_string(a.type_name());
            out_string(b.type_name());
            out_string(c.type_name());
            out_int(eq);
            out_int(i);
            i <- eq.copy();
            out_int(i);
            instr <- in_string();
            out_string(instr);
            inint <- in_int();
            out_int(inint);
            out_int(hello.length());
            hello <- hello.concat(hello);
            out_string(hello);
            out_int(hello.length());
            out_string(hello.substr(1, 5));
            abort();   
        }
    };
    
};
class A inherits IO {
    a : Int <- 222;
    methodA() : Object {
        out_string("A\n")    
    };
    methodOverride() : Object {
        out_string("A\n")      
    };
};
class B inherits A{
    b : Int <- 333;
    methodB() : Object {
        out_string("B\n")      
    };
    methodOverride() : Object {
        out_string("B\n")      
    };
};
class C inherits B{
    c : String <- "Hello World!";
    methodC() : Object {
        out_string("C\n")    
    };
    methodOverride() : Object {
        out_string("C\n")      
    };
};