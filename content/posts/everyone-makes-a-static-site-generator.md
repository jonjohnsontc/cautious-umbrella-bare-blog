---
date: 2023-07-25
title: Everyone Makes a Static Site Generator
description: And I am no exception. This is a tale about me and my own static site generator which now backs this website.
license: commercial
draft: true
---

I heard Jared Santo on The Changelog [mention](https://changelog.com/podcast/546#transcript-176) that every developer makes a Static Site Generator ("SSG"), almost as a right of passage to become an adult, and I too, had recently decided that now would be the time I *blossomed* into dev-adulthood.

## Background

For as long as I've had this blog, I've used Gatsby as my framework of choice. Early on, I decided that I wanted to use something that was easy to understand and that enabled me to do cute things that I saw on other developer websites. Which is to say, interactive *good* feeling web components you'd see shared on frontend focused developer blogs like joshwcomeau.com or kentcdodds.com  I've used Medium in my previous career to blog, and I always wanted that touch of something special, which told people that not only was I *professional*, but good professional worthy of the magic validation that comes from your peers when you make websites like that.

Now's the time for you to tell me, "But Jon, you can do kewl, interactive, attractive web components in (virtually) any web stack, all it takes is some elbow grease and a great idea"[^1]. And yes, that's true, but Jon from a few years back is a different person compared to Jon from now. And Jon from back then didn't have a foundation for web technologies that Jon has now, and Jon has now wants to stop writing in third person.

Gatsby has been in the static site gen-o-sphere since 2015. It marries a number of popular js libraries together (React, React Router, and GraphQL, most notably) for a developer experience that makes painting within the lines *super nice*. The happy path in Gatsby of creating page components with JSX, and creating dynamic content in MDX is easy to follow. You marry that with some component-driven development ("COD"), and I'm sure you can generate some fantastic 2018-era recommendations on how someone should make a static site.

CDD is a practice that I encountered on my first professional front-end code base, and observed when digging into different web applications in github for reference. And it happens to be what I tried using as well on my static site. When I refer to CDD, I'm talking about the approach to building UI from small components, typically written in its own file like a Java class. The small components build into other components, eventually coming together into a view component that represents the page.

For every month that went by, an average of one article idea came into my head, or perhaps an idea of some subtle improvements to my About Me page, and with that, at least one or two single page components would get added to my git tree. Unfortunately, I didn't have the interest and/or discipline to continue working on these ideas, and they languished quickly after being created. Sometimes, I would just quit on an idea after realizing that I needed a stronger base of knowledge of each layer of abstraction in my codebase. How can I complete displaying that SVG icon properly, with the correct colors given the site's theme, if I don't understand how Gatsby, React, and GraphQL work with their underlying web primitives? There were some problems with my website that I realized I couldn't npm install my way out of. And I managed to `npm install` my way into a few more problems whenever a major upgrade of these pillars came around.

Pretty soon, while my website was still devoid of content, my blog's repository continued to grow, with abandoned components littering my folder structure to greet me every time I lied to myself and said "TODAY, I WILL PRODUCE CONTENT". And looking at all of those files was a *pain*. Yes, it was a pain of my own creation, and probably nothing that a few solid minutes of pruning and serious reflection couldn't solve. But, it was a pain that produced enough anxiety to really distract from writing. I eventually stopped thinking about article ideas, and moved on to something else to scratch my creative itch.

Some months later, I witnessed some shots fired in the *Great React Debate of 2023*, and felt a renewed sense of motivation to work on my website. Why, many large voices in the web world were writing that I didn't need React. And, what better source of meaning(less) content then a full rewrite of something that I built earlier? Seriously though, I did read through several posts, along with heated hacker news threads following the saga, and did realize that maybe all of the additional abstractions I had signed-up for with a component driven Gatsby environment wasn't worth it for as small as my site is, especially since I haven't been in a front-end focused role for a few years now.

This isn't an anti-React/Gatsby, or anti-component driven design post. The technologies and approach both have their completely valid use cases, but I realized for myself that the trade offs involved with using them given my own situation wasn't worth it.

For this react-less rewrite, I deliberated between using an established static site generator like 11ty or Hugo, crafting my own static site generator in a language of my choice, or just handrolling html and javascript.

I can't remember when I first got the idea to make my rebuild framework-less. But, at some point during the great react debate, I stumbled across a blog post with someone detailing their own website's setup. They mentioned that it was just some html pages with a script tag linked. No build step required, no frameworks or additional layers of abstraction.

## A Tiny Site Tour

[Here's](https://github.com/jonjohnsontc/cautious-umbrella-bare-blog) the sites git repo.

Right now, it's bare bones, and only appeals to the few needs that I wrote down on the combined RFC+Jira Board+README that is my README file. Essentially, I have python script `render_templates`, that iterates through markdown-based content files, and combines them with jinja templates to produce a bunch of web pages in the `public` directory. There's a local store that I rely on, to check whether or not a content file has been modified since the script was last run. If so, the script creates a new version of the html page in `public`.

In terms of scripting, I have a bit of javascript in a `script.js` file that's linked to every page. It powers the lil theme dropdown menu above, and allows you to change the colors that the website appears in. Those details are saved across sessions using [localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage).

I also use a small python script to run as my development server if I need it (`server.py`). I find myself reaching for it a lot more often than just clicking on an html file in the Finder app for checking my pages out.

And that's about it. There's no other content management to speak of. I don't have any support for images yet...and I think I'm okay with that now? I realize that after spending so much time starting and never finishing anything on my site before, that any work-in-progress on this bad-boy is worth publishing. The site is living, so it can improve over time. Maybe you'll be reading this in 2 years and see that there's some cute swirling pig animation that whistles when you click it adorning the top of this page. Or really any other piece of visual content. It wasn't there when this article was first published. So, thanks for stopping by after it's improved.

[^1]: That and talent. I have zero-discernible drawing skills, and am not making anything that looks remotely as nice as the illustrations and animations they put out.
