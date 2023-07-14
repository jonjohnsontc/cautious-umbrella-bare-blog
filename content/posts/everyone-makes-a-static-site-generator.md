---
date: 2023-07-15
title: Everyone Makes a Static Site Generator
description: And I am no exception. This is a tale about me and my own static site generator which now backs this website.
license: commercial
draft: true
---

# Every (Programmer) Makes a Static Site Generator

And I am no exception. This is a tale about me and my own static site generator which now backs this website.

I heard Jared Santo on The Changelog [mention](https://changelog.com/podcast/546#transcript-176) that every developer makes a static site generator, almost as a right of passage to become an adult, and I too, had recently decided that now would be the time I *blossomed* into dev-adulthood.

## Background

For as long as I've had this blog, I've used Gatsby as my framework of choice. Early on, I decided that I wanted to use something that was easy to understand and that enabled me to do cute things that I saw on other developer websites. Which is to say, interactive *good* feeling web components you'd see shared on frontend focused developer blogs like joshwcomeau.com or ...  I've used Medium in my previous career to blog, and I always wanted that touch of something special, which told people that not only was I *professional*, but good professional worthy of the magic validation that comes from your peers when you make websites like that.

Now's the time for you to tell me, "But Jon, you can do kewl, interactive, attractive web components in (virtually) any web stack, all it takes is some elbow grease and a great idea". And yes, that's true, but Jon from a few years back is a different person compared to Jon from now. And Jon from back then didn't have a foundation for web technologies that Jon has now, and Jon has now wants to stop writing in third person.

Gatsby has been in the static site gen-o-sphere since 2015. It marries a number of popular js libraries together (React, React Router, and GraphQL, most notably) for a developer experience that makes painting within the lines *super nice*. The happy path in Gatsby of creating page components with JSX, and creating dynamic content in MDX is easy to follow. You marry that with some component-driven development, and I'm sure you can generate some fantastic 2018-era recommendations on how someone should make a static site.

CDD is a practice that I encountered on my first professional front-end code base, and observed when digging into different web applications in github for reference. And it happens to be what I tried using as well on my static site. I felt that it made 

For every month that went by, an average of one article idea came into my head, or perhaps some subtle improvements to my about me page, and with that, at least one or two single page components would get added to my git tree. Unfortunately, I didn't have the interest and/or discipline. 

Pretty soon, while my website was still devoid of content, my blog's repository continued to grow, with abandoned components littering my folder structure to greet me every time I lied to myself and said "TODAY, I WILL PRODUCE CONTENT". And looking at all of those files was a *pain*. Yes, it was a pain of my own construction, and probably nothing that a few solid minutes of pruning and serious reflection couldn't solve. But, it was a pain that produced enough anxiety to really distract from writing. I eventually stopped thinking about article ideas, and moved on to something else.

Some months later, I remember 

I can't remember when I first had the idea to make my own SSG, it may have been around the same time I read TKs post, where they mentioned their blog was a simple 

## Site Tour

Here's a link to the sites' git repo: https://github.com/jonjohnsontc/cautious-umbrella-bare-blog

Right now, it's bare bones, and only appeals to the few needs that I wrote down on the combined RFC+Jira+About that is the README file.
