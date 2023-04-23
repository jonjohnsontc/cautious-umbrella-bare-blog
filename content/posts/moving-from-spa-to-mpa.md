---
date: 2023-02-26
title: Moving from SPA to MPA
description: A lil story about how curiosity into the traditional server-side model also helped me gain some performance (and indirectly save some money) on a website of mine.
license: commercial
---

I've built a site called [Songwriter Graph](https://www.songwritergraph.org), which tries to map how songwriters write music in relation to one another. You can search for a songwriter, and it'll name their 5 most similar peers. It's been served via a big ol' bundle of Javascript from a Heroku Dyno ever since it was first deployed, but it was something that I've had regrets about. Mostly due to how I'd learned more about the web worked, with websites in the traditional server driven model, and indexing and discovery on search engines. Having a single-page application isn't ideal for a website which just indexes information it reads from a db, as no pages need to be dynamically generated. So, I found some time in-between a million other side-projects to explore the traditional server side model with my website, on a framework that I'd been hearing a lot about recently, Remix.

In this piece, I'll talk about how I first built the site, and some of the bigger conceptual changes that I had to translate into code. Afterwards, I'll talk about some performance differences I recorded with Lighthouse after deploying a version of the site to fly.io. You can jump to sections using the helper here, or just follow along.

## Why Remix?

I see these as first and foremost, performance issues that I've written myself, and could fix while still operating within the languages and tools that I built the website in. But, my real objective here is to learn more about the traditional client-server model of the web, so I'm going to be motivated the most by touching a nice and shiny new framework ✨.

## Description of the App

You can search for a songwriter via the search bar, and if they're indexed in the graph, you can load a profile of theirs. Each profile page contains some high level stats about the songwriter (key / tempo), along with a list of the top 5 most similar songwriters.

The data underlying the graph is ancient and fairly biased towards a couple genres. It only tops out at 10k songwriters, and 100,000 songs. So, it's very much a proof-of-concept. It demonstrates what I hope is possible with a bunch of music related data and songwriter credits - a system to help people discover songwriters they might not normally encounter based on what they listen to.

## How SWG was Deployed

The app was previously served as a big ol' bundle of Javascript from a Heroku Dyno. The bundle being built from clojurescript - specifically with reagent, self-described as a minimalistic React for clojurescript, along with re-frame a view library to help ensure a stateful UX. Underneath the hood, the API that served the songwriter info was built in Flask, leveraging SQLAlchemy as an ORM to chat with the data sitting in a SQLite db.

I made the choice to build the site as a [single-page application](https://developer.mozilla.org/en-US/docs/Glossary/SPA) (SPA) in cljs, because it mirrored the architecture of an application that I was working on at my job. The app I worked on at the time wasn't functionally similar to the graph at all, but I didn't have any other frontend experience at the time, and felt like the easiest way to get up and moving.

In the time since I initially deployed the site, I've learned a whole lot more about the traditional client-server model on the web, and figured the songwriter graph would be a much better fit for that setup.

## Redesign of the Application

Changing the graph from an SPA to server driven experience felt approachable. After taking a second to re-orient myself with the site's codebase, I realized that I really only needed to re-create the views and api queries + db calls. The rest of the code base, which was made up of logic surrounding how the site functioned was unnecessary. This is because that logic was there to help navigate users between writers, which was automatically baked into the back/forward buttons of the standard web.

In terms of recreating the views & queries + api calls, it required a slight reshuffling of concepts in my head, which we'll get into below.

### Views + Routes

Keeping the 'single' in single page application, all views within the app (writer/search/about) were encompassed in a single `views.cljs` file. Conversely, each is manifested as a separate [route](https://remix.run/docs/en/v1/guides/routing#defining-routes) page within Remix.

Each of these routes performs the same task as the views, rendering components for the given page of the graph, dynamically based on the search term or id passed in the url params. However, the routes in Remix also load the data required for the page (like writer details) via a `LoaderFunction`.

This replaces the REST API that I left for anyone to peruse/abuse, which I think could potentially save me money in the long run.

### The Database & App 'State'

This brings me to the other 'big' conceptual change, managing calls to the db to retrieve the correct details to fill out a page. In the SPA, I constructed some SQL queries (using SQLAlchemy as an ORM layer) to pull writer details depending upon the context. Afterwards, I created some REST API endpoints to serve this data to the user when they request a page.

With Remix, the LoaderFunction I mentioned before acts as both the REST endpoint and the db call. Which doesn't shave a ton of code, but I think makes the intent easier to read when coming back to the codebase after some time.

## Performance Differences

I expected a fair decrease in initial page load from the application, because the graph was previously just one bundle of javascript, and everything was set to load at once. The scores from Lighthouse showed even greater gains than I had expected:

### Desktop

| Category                 | SPA   | Remix |
| ------------------------ | ----- | ----- |
| First Contentful Paint   | 3.4 s | 0.5 s |
| Time to Interactive      | 3.5 s | 0.8 s |
| Speed Index              | 3.4 s | 0.5 s |
| Total Blocking Time      | 30 ms | 0 ms  |
| Largest Contentful Paint | 3.4 s | 0.8 s |
| Cumulative Layout Shift  | 0.004 | 0.002 |

### Mobile

| Category                 | SPA    | Remix |
| ------------------------ | ------ | ----- |
| First Contentful Paint   | 18.0 s | 1.8 s |
| Time to Interactive      | 18.6 s | 2.7 s |
| Speed Index              | 18.0 s | 1.8 s |
| Total Blocking Time      | 390 ms | 0 ms  |
| Largest Contentful Paint | 18.1 s | 2.7 s |
| Cumulative Layout Shift  | 0.002  | 0.002 |
