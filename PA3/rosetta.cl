-- COOL: Reverse-sort the lines from standard input. 

Class Main -- Main is where the program starts
  inherits IO { -- inheriting from IO allows us to read and write strings

	main() : Object { -- this method is invoked when the program starts
             let 
                 edges : List <- new Nil, -- the sorted list input lines
      			 vert : List <- new Nil,
      			 s : List <- new Nil,
      			 l : List <- new Nil,
                 done : Bool <- false, -- are we done reading lines? 
      			 n : String <- "",
                 m : String <- "",
                 curr : List <- new Nil,
                 prev : List <- new Nil,
                 first : Bool <- true,
                 cycle : Bool <- false
             in {
               while not done loop {
                 let s_a : String <- in_string(), s_b : String <- in_string() in
                 if s_b = "" then (* if we are done reading lines
                                 * then s will be "" *) 
                   done <- true 
                 else 
                   edges <- edges.insert(s_a, s_b) -- insertion sort it into our list
                 fi ;
               } pool ; -- loop/pool deliniates a while loop body
               --edges.print_list () ; -- print out the result
               --out_string("***\n***\n") ;
               vert <- edges.get_vertices(vert) ;
               --vert.print_list() ;
               --out_string("***\n***\n") ;
               s <- vert.get_s(edges, s) ;
               --s.print_list() ;
               
               if (s.empty()) then
                  {
                  cycle <- true;
                  }
               else
               	  true
               fi ;
               
               while not (s.empty()) loop
               {
                  --out_string("\n*****\n");
                  --s.print_list();
                  --out_string("*****\n");
                  n <- s.get_string_a();
                  s <- s.pop_front();
                  l <- l.append(n);
                 
                  curr <- edges;
                  first <- true;
                  while not curr.empty() loop {
                    if curr.get_string_b() = n then 
                    {
                       m <- curr.get_string_a();
                       if first then
                          edges <- curr.get_next()
                       else
                          prev.set_next(curr.get_next())
                       fi ;
                       if not edges.incoming_edge(m) then 
                          s <- s.insert(m, "")
                       else
                         true
                       fi ;
                      curr <- prev;
                    }
                    else
                       true
                    fi ;
                    prev <- curr;
                    curr <- curr.get_next();
                    first <- false;
                  } pool ;
                 
               }
               
               pool ;
               if not edges.empty() then
               {
                  cycle <- true;
                  --edges.print_list();
               }
               else
                  true
               fi ;
               if cycle then
                  out_string("cycle\n")
               else
                  l.print_list()
			   fi ;
               (*if l.contains("----") then
               	  out_string("true")
               else
               	  out_string("false")
               fi ;*)
               --out_string("DONE") ;
             }
	};
};

(* The List type is not built in to Cool, so we'll have to define it 
 * ourselves. Cool classes can appear in any order, so we can define
 * List here _after_ our reference to it in Main. *) 
Class List inherits IO { 
        (* We only need three methods: cons, insert and print_list. *) 
           
        (* cons appends returns a new list with 'hd' as the first
         * element and this list (self) as the rest of the list *) 
	cons(ha : String, hb : String) : Cons { 
	  let new_cell : Cons <- new Cons in
		new_cell.init(ha, hb,self)
	};

        (* You can think of List as an abstract interface that both
         * Cons and Nil (below) adhere to. Thus you're never supposed
         * to call insert() or print_list() on a List itself -- you're
         * supposed to build a Cons or Nil and do your work there. *) 
	insert(i : String, j : String) : List { self };
  	contains(i : String) : Bool { false };
  	get_vertices(vert : List) : List { self };
  	get_s(edges : List, s : List) : List { self };
  	incoming_edge(vertex : String) : Bool { false };
  	empty() : Bool { true };
  	pop_front() : List { self };
  	get_string_a() : String { "" };
  	get_string_b() : String { "" };
  	append(i : String) : List { self };
    get_next() : List { self };
    set_next(l : List) : List { self };
	print_list() : Object { abort() };
} ;

Class Cons inherits List { -- a Cons cell is a non-empty list 
	xa : String;          -- xa is the first string of the list head 
  	xb : String;		  -- xb is the second string of the list head()
  						  -- xb will be "" if this is a vertex instead of an edge
	xcdr : List;            -- xcdr is the rest of the list

	init(ha : String, hb : String, tl : List) : Cons {
	  {
	    xa <- ha;
        xb <- hb;
	    xcdr <- tl;
	    self;
	  }
	};
	  
        (* insert() does insertion sort *) 
	insert(s_a : String, s_b : String) : List {
		if not (xa < s_a) then          -- sort in order
			(new Cons).init(s_a, s_b, self)
		else
			(new Cons).init(xa, xb, xcdr.insert(s_a, s_b))
		fi
	};
  		(* contains() looks at the first tuple and checks if i matches any in the list *)
	contains(i : String) : Bool {
        if (xa = i) then
        	true
        else
        	xcdr.contains(i)
		fi
    };
    		(* gets a list of all the vertices *)
  	get_vertices(vert : List) : List { 
  	{
      if not vert.contains(xa) then
      	  vert <- vert.insert(xa, "")
      else
      	  true
      fi ;
      if not vert.contains(xb) then
      	  vert <- vert.insert(xb, "")
      else
      	  true
      fi ;
      vert <- xcdr.get_vertices(vert) ;
    }
  
   };  		
  		(* gets the list s *)
   get_s(edges : List, s : List) : List { 
     {
       if not (edges.incoming_edge(xa)) then
       	  s <- s.insert(xa, "")
       else
       	  true
       fi ;
       s <- xcdr.get_s(edges, s);
     }
     
   };
   incoming_edge(vertex : String) : Bool { 
     {
       if (xa = vertex) then
       	  true
       else
       	  xcdr.incoming_edge(vertex)
       fi ;
     }
     
   };
   empty() : Bool { false };
   pop_front() : List { xcdr };
   get_string_a() : String { xa };
   get_string_b() : String { xb };
   append(i : String) : List {
      (*if (xcdr.empty()) then         
			(new Cons).init(i, "", self)
		else
			(new Cons).init(xa, xb, xcdr.append(i))
		fi*)
     (new Cons).init(xa, xb, xcdr.append(i))
       
     
   };
   get_next() : List { xcdr };
   set_next(l : List) : List { 
   {
     xcdr <- l;
     self;
   }
  };
  

  

  
  

	print_list() : Object {
		{
		     out_string(xa);
          if not (xb = "") then
          	 {
          	 out_string(", ");
          	 out_string(xb);
             }
          else
          	 true
          fi;
		     out_string("\n");
		     xcdr.print_list();
		}
	};
} ;

Class Nil inherits List { -- Nil is an empty list 

	insert(s_a : String, s_b : String) : List { (new Cons).init(s_a, s_b, self) }; 
  	contains(i : String) : Bool { false };
  	get_vertices(vert : List) : List { vert };
	get_s(edges : List, s : List) : List { s };
    incoming_edge(vertex : String) : Bool { false };
    empty() : Bool { true };
  	pop_front() : List { self };
    get_string_a() : String { "" };
  	get_string_b() : String { "" };
    append(i : String) : List { (new Cons).init(i, "", self) };
  	get_next() : List { self };
    set_next(l : List) : List { self };

	print_list() : Object { true }; -- do nothing 

} ;

