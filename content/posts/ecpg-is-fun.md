---
date: 2024-09-22
title: ECPG is fun
description: TIL about Embedded SQL 
license: commercial
code: true
---

I've come to really appreciate SQL, and how it has come to be the common interface for accessing data in a table, even if that table isn't stored in a relational database. There's tradeoffs though, many times you have to run the query before knowing if the syntax is correct, and you generally have to make some sort of mapping between the SQL and whatever language you've chosen to do all the other fun stuff.

An ORM is one approach to handling the problem differently. I came across these when I started working on web applications, where my team had used it to handle the operations that users were able to do on our fancy dashboard generator&trade;, and turn them into queries against postgres. This model comes with another set of tradeoffs that much smarter and experience developers can extol on.

Thanks to a Hackernews comment[^1], I learned of a SQL-first approach to marrying the querying interface with a programming language, and that's Embedded SQL. It's a method defined in the SQL standard of writing queries inline in a host language, and then having a preprocessor transform those that code into valid *host language source code*&trade; that can be compiled and run like any other program.

God's favorite RDBMS <strike>SQLite</strike> Postgres provides a way of using embedded SQL through ECPG, which has been part of the database since version 6.3[^2]. As long as your language of choice happens to be C or C++ , you can use it to build your own programs. With a brief[^3] read through of the docs, one can come up with a pretty trivial example that gives returns a scalar for a simple query.

    :::c
    EXEC SQL WHENEVER SQLWARNING SQLPRINT;  // print SQL warnings to console 
    EXEC SQL WHENEVER SQLERROR STOP;  // terminate program on SQL runtime err

    EXEC SQL BEGIN DECLARE SECTION;
      const char *pword = getenv("POSTGRES_PASSWORD");
      const char *user = "jon";
      const int filter = 4;
      const char *dbname = "unix:postgresql://localhost:5433/ecpg_demo";
      long long int count
    EXEC SQL END DECLARE SECTION;  

    if (pword == NULL) {
      fprintf(stderr, "Env var not found\n");
      exit(1);
    }

    EXEC SQL CONNECT TO :dbname USER :user USING :pword;  
    printf("SQL connection executed\n");  
    EXEC SQL SELECT count(*) INTO :count  
    FROM electricity_market  
    WHERE weekday = :filter;  
    printf("Total number of rows in electricity_market: %d\n", count);  

The console would show:

    :::console
    jon@wendy:~/projects/ternary-implosion$ ./main 
    SQL connection executed
    Total number of rows in electricity_market: 6288

You can iterate over multiple results while using a cursor, and there is a header for handling Postgres types that can't be expressed in C primitives. This makes un-marshalling / handling data between the application and db far more trivial. In the example below, the `electricty_market` table has a number of columns which require arbitrary precision, so they use the postgres 'numeric' type.

    :::c
    #include <pgtypes_numeric.h>
    EXEC SQL BEGIN DECLARE SECTION;
      numeric *hydro_gen;
      int *hydro_gen_ind;
    EXEC SQL END DECLARE SECTION;

    // use cursors for iterating over a result set
    EXEC SQL DECLARE cur CURSOR FOR
      SELECT miso_gas_gen FROM electricity_market
      ORDER BY miso_gas_gen;
    EXEC SQL OPEN cur;
    EXEC SQL FETCH NEXT FROM cur INTO :hydro_gen INDICATOR :hydro_gen_ind;  
    EXEC SQL CLOSE cur;
    
    // else you can run into a SQL ERROR if the value is NULL 
    if (*hydro_gen_ind < 0)
      printf("miso_gas_gen was NULL\n");
    else
      printf("miso_gas_gen is %s\n", PGTYPESnumeric_to_asc(hydro_gen, -1));

shows

    :::console
    miso_gas_gen is 6314.58

The preprocessor step also provides checking to make sure the query is syntactically correct. I found this to be helpful, and caught a few silly mistakes before passing it off to postgres. It's not going to be able to tell you if a query can successfully execute, however, because it doesn't validate the tables or columns referred. I still think this is a step up from *zero* SQL checking, although you never want to be stuck in the sad cycle of fixing SQL build errors, C build errors, and SQL runtime errors when building queries[^4].

When it comes to SQL runtime errors, by default there is no handling. You can silently trigger an error through one query tied to a bound parameter, and that could propagate to all other queries in your program that use it. To prevent this, we can set callbacks to the top of the program, like in the first example. They allow some simple actions to be taken in case of an error, like terminating the program, or jumping to some labelled part of it. There is also a `sqlca` (SQL communication area) struct that's exposed which gives you more control over exactly what you can do. It behaves much like `errno` does in C, meaning if there's multiple errors in your SQL code it will only contain information about the last one[^5].

I don't know how much embedded SQL has ever caught on. Word is that historically programs compiled through ECPG were less performant, as dynamic optimization was difficult for compilers using generated code[^6]. Comparing the performance of a non-trivial application using embedded SQL and code using libpq could be an interesting exercise.  

I guess the "fun" part of my experience with ECPG has been learning about the ways that standards bodies and developers have worked on bridging the gap between SQL and the programming language glue that's needed to for interaction between data and the rest of the application. Most of the work surrounding embedded SQL seems to have occurred around 30 years ago. Sometimes I'm doing exploratory work against tables I'm not super familiar with, and I still don't even have the lowest form of SQL syntax linting before I submit queries off. So, it's given me an appreciation of the facilities that are available to me as a developer using Postgres in applications, and just how big the SQL standard is.

[^1]: <https://news.ycombinator.com/item?id=41478930>
[^2]: <https://www.postgresql.org/docs/release/6.3.0/>
[^3]: For you, not me. I spent a few hours futzing with the connection string before a helpful StackOverflow post helped me realize that just *maybe* my demo postgres instance wasn't listening on port 5432.
[^4]: I'm totally guessing here, but I imagine that exploratory data analysis is probably not something you would do using ECPG. I imagine it's been used for different class of problems traditionally.
[^5]: <https://www.postgresql.org/docs/current/ecpg-errors.html#ECPG-SQLCA/>
[^6]: <https://www.quora.com/Does-anyone-still-actively-write-Embedded-SQL/>
