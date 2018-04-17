class Main inherits IO {
    a : Int <- 50;
    b : Int;
    c : Int;
    d : D;
    newD : D;
    e : E;    
    main() : Object {{
    
    
    d <- (new D).init("D");
    d.print();
    
    while 0 < a loop
    {
            d.print();
            a <- a - 1;
    }
    pool;
    
    newD <- d.get_new("newD"); 
    newD.print();
    
    newD.dispatch(new D);
    e <- new E;
    e@D.print();
    (new E)@D.print();
    
    }};
};
class D inherits IO {
    str : String;
    overall : String;
    
    init(inputstr : String) : SELF_TYPE {{
            str <- inputstr;
            self;
    }};
   
    print() : SELF_TYPE {
        {
            overall <- overall.concat(str.concat("\n"));
            out_string(str);
            self;
        }
    };
   
    get_new(inputstr : String) : D {{
        out_string((new D).type_name());
        (new D).init(inputstr);
        
    }};
    
    dispatch(inp : D) : Object {
        {
            inp.print();
            self;
        }
    };
   
  
};

class E inherits D {
       
    print() : SELF_TYPE {
        {
            overall <- overall.concat(str.concat("\n"));
            out_string(overall);
            self;
        }
    };
      
  
};

