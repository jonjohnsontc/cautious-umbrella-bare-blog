---
date: 2025-01-02
title: Recommended Reading - PostgreSQL Query Optimization 
description: I recently read "PostgreSQL Query Optimization:\ The Ultimate Guide to Building Efficient Queries" and think it's a great resource for helping to build a better intuition on how to query postgres effectively
license: commercial
draft: false 
---

If you're looking to learn a about how to craft queries in PostgreSQL effectively, you have a loads of documentation, lessons, and LLMs to query that you can find on the internet. I found myself in a similar spot recently, I've spent some time working through attempting to optimize individual queries through a combination of trial and error, EXPLAIN ANALYZE, praying to foundational models, and mentioning to all my colleagues about how much better _my_ DDL would've been if only I had been given a chance to design all the tables with the benefit of years of hindsight. But, I was looking for a framework for understanding how to better craft queries in the first place, because that can save a lot of those aforementioned issues, and help save my colleagues sanity.

I recently read 2024's "[PostgreSQL Query Optimization: The Ultimate Guide to Building Efficient Queries](https://link.springer.com/book/10.1007/979-8-8688-0069-6)", in an effort to do so, and I think it's worth your time if you're looking for something similar. At 344 pages, it's a pretty a pretty small and approachable text for building queries in a way that works with PostgreSQL as opposed to working against it. It's also less than 11% of the size of PostgreSQL's current documentation, so it allows you to develop a working model of some optimization concepts in an 80-20-like approach. It also includes links to download a postgres_air schema, a schema for a fictional airline which forms the basis of all queries in the book.

## Book Overview

The book follows a nice flow, which starts with some baseline information on why to improve query execution time, as well as some intiuition in _how_ to set and measure optimization goals. It then digs into some basic relational theory, and loosely breaks down the stages of query execution in postgres. All of this culminates with a chapter on execution plans that can be referenced throughout the remainder of the book.

The next part of the book delves into optimization for the two major types of queries, short and long, and the considerations that need to be made for DML (data modification) queries. Afterwards, it takes a brief look at the effects of some noteworthy configuration parameters. The remainder of the book is spent on optimizing an application's performance that leverages a database, and why one should prefer using functions and dynamic SQL as opposed to an ORM layer to define the contract between the app and db. At the very end, the authors wrap things up by providing a flow-chart for optimizing an arbitrary query using the information previously explored.

## Lessons Learned

I want to touch on a few points in particular that I've learned and hope will stick with me:

### 1. The Difference in Optimizing Short and Long Queries

Prior to reading this book, I might've heard of _short_ and _long_ queries, but certainly hadn't a clue of their individual intricacies when attempting to optimize them. The terms _short_ and _long_ refer to the number of rows that need to be scanned relative to the size of the tables in order to provide a result for a query. 

Depending on the type of query you have to optimize, you're looking at a slightly different path of potential modifications. Ensuring that we execute the most restrictive filter or join is often the most important, but the considerations can change up quite a bit from there. If you have a short query for instance, properly set indexes can be a huge performance multiplier. Properly set meaning, they provide coverage for the parameters being filtered and joined on[^1].

Long queries, on the other hand can benefit from decisions beyond metadata or table structures. Those of us familiar with OLAP workflows can speak to the benefits of taking some long query and dividing it up amongst a set of incremental updates. We also are gonna be much less reliant on indexes, since a long query by definition is going to be scanning a huge portion of a table. So, making sure that we can setup queries in such a way so that we only scan large tables once can be a huge boon. I think one of the most illustrative examples is from when the author mentions using a VIEW in a large query. The VIEW is being joined against a large table, and results in several large sequental scans against the large table due to how the VIEW was initially built[^2]. Decoupling the long query from the VIEW resulted in massive performance gains

I'm really just scratching the service here. The book presents a number of scenarios and optimizations to consider depending on the query type.

### 2. Configuration can do great harm, and most optimization wins will come from elsewhere

The authors don't spend much time on PostgreSQL configuration parameters, and they state that more impactful optimizations can generally be found elsewhere[^3]. On other side of the coin, however, a mis-configured postgres instance could result increased query times and much lower reliability. The authors point to an example of setting `work_mem` (working memory) to some level
that would cause users to see OOM errors if the `max_connections` setting is too high. Postgres isn't going to do the math for you to see if every single connection is max_connections would have enough work_mem available to them.

### 3. The Benefits of Dynamic Query Execution

Unlike say Oracle, Postgres saves the optimization step in query execution for as late as possible. This allows the db to take into account table statistics for dynamic query elements. For instance, say you have a parameterized query in your application to pull users data out, and it's based on some filter, like the users' home country, postgres is going to return an optimized query plan that's probably going to work _really well_ if the filter condition has high selectivity (represents a low % of rows). Like pulling users in Turkmenistan vs a similar parameterized query in Oracle for your international app.

### 4. NORM as an ORM

NORM (aka No-ORM) is an approach to mapping application data to its database in a more "database focused" way than what's typically seen by ORM-backed applications. ORM's can result in fairly succinct code on the application side of things, but they can lead to an applicaton making several database calls for a group of objects that it very well could've done in a single well-formed query (often referred to as the N+1 query problem).

NORM is backed by a JSON schema that defines a contract between the database and the application objects. Through this schema, objects created can be serialized to JSON, and sent to the database to be executed as a query. Once the JSON is submitted to the database, a function parses the JSON, and executes the necessary transaction. This really flips the ORM approach by making the database responsible for decomposing the object into database updates, as opposed to having the ORM make a number of small queries on behalf of the application to update the database. 

The authors include a link to the [NORM](https://github.com/hettie-d/NORM) framework on GitHub, which includes a set of packages that can automate building out NORM functions for your application. There is also a user guide which dives much deeper than this blog post (and the book).

## Verdict

All-in-all, If you're looking to build a better mental model of Postgres, and how to build postgres friendly queries, I'd highly recommend it. The examples make take some time to walk all the way through if you're following along with your own postgres instance, but feels well worth the time[^4]. 

[^1]: One thing in particular that seems obvious in hindsight, is that indexes don't provide any peformance benefit if your query is applying some transformation to the index in question. If you have an index on an `updated_date` column, and then filter data in your query by using `MONTH(updated_date)` the query engine isn't going to leverage the index at all.
[^2]: [https://learning.oreilly.com/library/view/postgresql-query-optimization/9798868800696/html/501585_2_En_7_Chapter.xhtml#:-:text=Views%3A%20To%20Use,they%20cause%20problems%3F](https://learning.oreilly.com/library/view/postgresql-query-optimization/9798868800696/html/501585_2_En_7_Chapter.xhtml#:-:text=Views%3A%20To%20Use,they%20cause%20problems%3F)
[^3]: Particularly vs actually adjusting the query joins and filters: [https://learning.oreilly.com/library/view/postgresql-query-optimization/9798868800696/html/501585_2_En_10_Chapter.xhtml#:-:text=Although%20some%20parameter,hundreds%20of%20times](https://learning.oreilly.com/library/view/postgresql-query-optimization/9798868800696/html/501585_2_En_10_Chapter.xhtml#:-:text=Although%20some%20parameter,hundreds%20of%20times)
[^4]: This isn't Joe Celko's SQL for Smarties, you can get through the text and run all the examples in recreationally paced week.