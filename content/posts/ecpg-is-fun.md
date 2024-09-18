---
date: 2024-09-17
title: ECPG is fun
description: TIL about Embedded SQL 
license: commercial
draft: true
---

I've come to really appreciate SQL, and how it has come to be the common interface for accessing data in a table, even if that table isn't stored in a relational database. There's tradeoffs though, many times you have to run the query before knowing if the syntax is correct, and you generally have to make some sort of mapping between the SQL and whatever language you've chosen to do all the other fun stuff.

An ORM is one approach to handling the problem differently. I came across these when I started working on web applications, where my team had used it to handle the operations that users were able to do on our fancy dashboard generator (tm). This model comes with another set of tradeoffs that much smarter and experience developers can extol on.

I recently learned of another, more brute force approach to marrying the querying interface with a programming language, and that's Embedded SQL. It's a method defined in the SQL standard of writing queries inline in a host language, and then having a preprocessor transform those that code into valid(tm) host source code that can be compiled and run like any other program.

God's favorite RDBMS <strike>SQLite</strike> Postgres provides a way of using embedded SQL through ECPG, which has been part of the db since version 6.3[^1]. As long as your language of choice happens to be C or C++ , you can use it to build your own programs. With a brief[^2] read through of the docs, one can come up with a pretty trivial example that gives you 

[^1]: https://www.postgresql.org/docs/release/6.3.0/
[^2]: For you, not me. I spent a few hours futzing with the connection string before a helpful SO post helped me realize that just maybe my demo postgres instance wasn't listening on port 5432.