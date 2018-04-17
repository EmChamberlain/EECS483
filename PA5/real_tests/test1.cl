class Main inherits IO {
    a : A <- new A;
    b : B <- new B;
    c : C <- new C;
    attra : Int <- 1001;
    attrb : Int <- 1002;
    attrc : Int <- 1003;
    main() : Object {{
        a.let_scope();
        --scoping for let
        let attra : Int <- (1 +(2 /(3 - (4 * (8) / 4)) + 1) *2) in
        {
            --scoping for case
            case a of 
            attra : A => attra.check();
            attra : B => attra.check();
            attra : C => attra.check();
            esac;
            
            case b of 
            attra : A => attra.check();
            attrb : B => attrb.check();
            attrc : C => attrc.check();
            esac;
            
            case c of 
            attra : A => attra.check();
            attrb : B => attrb.check();
            attrc : C => attrc.check();
            esac;
                      
            
            --check if further calls get contaminated
            case c of 
            attrc : C => attrc.contaminated_args(a, b, attrc.attrcheck());
            esac;
            
            --check if other cases contaminated
            case c of 
            attra : A => attra.check();
            attrb : B => attrb.print(attra);
            attrc : C => attrc.print(attra);
            esac;
            
            
            --check nested cases
            case c of
            attra : Object =>
                case attra of
                attra : A => 
                    case attra of
                    attra : C => attra.check();
                    esac;
                attrb : B =>
                    case attrb of
                    attrb : C => attrb.check();
                    esac;
                esac;
            esac;
            
            
        };
    }};
};

class A inherits IO {
    a : Int <- 1;
    attra : Int <- 11;
    let_scope() : Object {
    let a : Int <- 10 in print(5)
    };
    
    print(a : Int) : Object {
        out_int(a)
    };
    
    check() : Object {
        out_int(a)
    };
   
};
class B inherits A {
    b : Int <- 2;
    
    print(b : Int) : Object {
    out_int(b)
    };
    
    check() : Object {
        out_int(b)
    };
};
class C inherits B {
    c : Int <- 3;
    attrc : Int <- 5;
    print(c : Int) : Object {
    out_int(c)
    };
    
    check() : Object {
        out_int(c)
    };
    
    contaminated_args(a : A, b: B, c : C) : Object{{
        a.check();
        b.check();
        c.check();
    }};
    attrcheck(): C {{
        out_int(attrc);
        self;
    }};
};