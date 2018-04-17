
class Main {
    x : Int <- y + 1;
    y : Int <- x + 1;
    w : Int;
    z : Int;
 main() : Int { {
        x + y;
        w + z;
        x + z;
        let var : SELF_TYPE in
            var.main() + y;
        x + y / 2 * 12 - w + 4;
    }};
   
};

class A {
    a : A;
    
    i : Int <- 6;
    j : Int;
    k : Int <- 11;

    a1(in1 : Int, in2 : Int) : Int { 
        in1 + in2
    };
    a2() : Int {
        8 + 4
    };
    a3() : SELF_TYPE {
        new SELF_TYPE
    };
};

class B inherits A {
    b : B;
    a1(in1 : Int, in2 : Int) : Int { 
        5 + 6
    };
    b1() : Int {
        a1(i, j) + b1()
    };
};

class C inherits B {
    c : C;
    a1 : A <- self@A.a3();
    c1() : Int {
        c.b1() + c1() + c@A.a1(j, k) + c@B.b1() + self@C.b1()
    };
    
    voidTest() : Bool {
        isvoid (self@A.a3())
    };
    
    case1() : Object { {
        case a of
            x : A => x.a1(b1() + 7, j);
            y : B => y.b1();
            z : C => z.c1();
        esac;
        
        case b of
            x : A => x.a1(i, j);
            y : B => y.b1();
            z : C => z.c1();
        esac;
        
        case c of
            x : A => x.a1(i, k);
            y : B => y.b1();
            z : C => z.c1();
        esac;
    }};
    
};


