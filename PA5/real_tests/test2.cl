class Main inherits IO {
    a : A <- new A;
    b : B <- new B;
    c : C <- new C;
    attra : Int <- 1001;
    attrb : Int <- 1002;
    attrc : Int <- 1003;
    main() : Object {{
        --scoping for nested lets
        let attra : Int <- (1 +(2 /(3 - (4 * (8) / 4)) + 1) *2) in
        {
            out_int(attra);
                out_int(attrb);
                out_int(attrc);
            let attrb : Int <- attrc in
            {
                out_int(attra);
                out_int(attrb);
                out_int(attrc);
                let attra : Int <- attrc in
                {
                    out_int(attra);
                    out_int(attrb);
                    out_int(attrc);
                    let attra : Int <- 50,
                    attrb : Int <- 60,
                    attrc : Int <- 70
                    in
                    {
                        out_int(attra);
                        out_int(attrb);
                        out_int(attrc);
                    };
                };
            };                       
        };
        --checking default values for let
        let b : Bool in 
        {
            if isvoid b
            then out_string("True")
            else out_string("False")
            fi;
        };
        
        --checking assigning variables in let
        let attra:  Int,
        attrb : Int,
        attrc : Int
        in
        {
            out_int(attra);
            out_int(attrb);
            out_int(attrc);
            attra <- 1;
            attrb <- 2;
            attrc <- 3;
            out_int(attra);
            out_int(attrb);
            out_int(attrc);
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