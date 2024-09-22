---
date: 2024-09-17
title: ECPG is fun
description: TIL about Embedded SQL 
license: commercial
draft: true
---

I've come to really appreciate SQL, and how it has come to be the common interface for accessing data in a table, even if that table isn't stored in a relational database. There's tradeoffs though, many times you have to run the query before knowing if the syntax is correct, and you generally have to make some sort of mapping between the SQL and whatever language you've chosen to do all the other fun stuff.

An ORM is one approach to handling the problem differently. I came across these when I started working on web applications, where my team had used it to handle the operations that users were able to do on our fancy dashboard generator (tm). This model comes with another set of tradeoffs that much smarter and experience developers can extol on.

Thanks to the time suck of a Hackernews comment, I learned of a SQL-first approach to marrying the querying interface with a programming language, and that's Embedded SQL. It's a method defined in the SQL standard of writing queries inline in a host language, and then having a preprocessor transform those that code into valid(tm) host source code that can be compiled and run like any other program.

God's favorite RDBMS <strike>SQLite</strike> Postgres provides a way of using embedded SQL through ECPG, which has been part of the db since version 6.3[^1]. As long as your language of choice happens to be C or C++ , you can use it to build your own programs. With a brief[^2] read through of the docs, one can come up with a pretty trivial example that gives returns a scalar for a simple query.

    :::postgres
    EXEC SQL CONNECT TO :dbname USER :user USING :pword;  
    printf("SQL connection executed\n");  
    EXEC SQL SELECT count(*) INTO :count  
    FROM electricity_market  
    WHERE weekday = :filter;  
    printf("Total number of rows in electricity_market: %d\n", count);  

The console would show:

    :::shell
    jon@wendy:~/projects/ternary-implosion$ ./main 
    SQL connection executed
    Total number of rows in electricity_market: 6288
    SQL connection exited

You can iterate over multiple results while using a cursor

The preprocessor step also provides checking to make sure the query is syntactically correct. I found this to be helpful, and caught a few silly mistakes before passing it off to the server. It's not going to be able to tell you if a query can successfully execute, however, because it doesn't validate the tables or columns referred. I still think this is a step up from zero SQL checking, although you never want to be stuck in the sad cycle of fixing SQL build errors, C build errors, and SQL runtime errors when building queries[^3].

Word is that historically programs compiled through ECPG were less performant, as dynamic optimization was difficult for compilers using generated code[^4].

[^1]: <https://www.postgresql.org/docs/release/6.3.0/>
[^2]: For you, not me. I spent a few hours futzing with the connection string before a helpful StackOverflow post helped me realize that just _maybe_ my demo postgres instance wasn't listening on port 5432.
[^3]: Exploratory data analysis is probably not something you would do using ECPG. I imagine it's been used for different class of problems traditionally.
[^4]: <https://www.quora.com/Does-anyone-still-actively-write-Embedded-SQL/>
