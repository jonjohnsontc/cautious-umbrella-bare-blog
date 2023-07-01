---
date: 2023-05-17
title: Drag Queens and the Godot Engine
description: 
license: commercial
draft: true
---
# Drag Queens and Godot

This past week marked my birthday, and to celebrate, I went out to RuPaul's Drag Con here in LA. I've never seen so many fabulous looking people in a single location. With House of Love cocktails to guide my friends and I, we were lucky to meet a few of our favorites while testing the limits of how intoxicated a group should be in public.

I also learned a bit about how games are constructed in the newest version of Godot, and started reading up on C++.

## A Drag themed trading card game

After completing a framework-less rewrite of my website[^1], I decided that it was time to start working on a game. And, to celebrate the timing of DragCon, I decided to make a drag themed card game in the style of Triple Triad. Triple Triad is a card battler originally from Final Fantasy VIII, but was re-tailored for Final Fantasy XIV some years later. There's also mobile and web game versions that I've seen in the wild that do and don't carry any fun likely unlicensed finaly fantasy ip[^2]. 

<details>
<summary>Click for a brief Triple Triad description</summary>
Two players play against one another, on a 3x3 board. Each come equipped to play with five cards of varying value. They take turns laying a card on the board. If a player lays their card to an adjacent competitors card, they battle, based on the cards values for their adjacent sides. The winner of the battle claims the other card, transforming ownership of the card to the other player. The winner of the game is the one who controls the most cards by the time the board has been filled (any unplayed cards count towards this total).
</details>

I spent some time deliberating how I would build out the game, before deciding on using the Godot Engine v4. The balance of approachability, and iteration speed with GDScript, along with the ability to compile to mobile and PC/Mac targets won me over :hugging_face:.

I haven't made much of a game yet, on startup you can move a card around` a pink bubbly background, and flip it around to show which player has 'control'.

```
    SHOW GIF OF CARD FLIPPING IN GAME
```

That being said, my efforts in learning and using Godot so far haven't been much more than a couple of afternoons. And, for that kind of progress I'm happy. The engine and included editor feel very much batteries included. I code most comforatably in vs code, but I haven't been looking to jump to it for editing any GDScript/.gd files. Games in the engine are comprised of a tree of nodes grouped together into scenes[^3]. Scenes can be built in the 2D or 3D editor by customizing nodes, and then you can drop down into the code editor to create a script that will execute the games logic by extending the nodes/classes used. 

My goal is to create a working demo of 'Triple Trial with Queens', where two players can play against each other using the same device. I'd like to create at least 10 unique cards for this demo, because I think it would look a little more polished than say, 2 copies each of five cards. Once finished, I can decide whether or not to take the idea further.

[^1]:Writeup coming soon
[^2]:I'm also not making this with the queens explicit permission, though I'd like to think if I build something of interest, perhaps it's something that could get packaged and sold to serve the queens :raised_hands: :queen:.
[^3]: [https://docs.godotengine.org/en/stable/getting_started/introduction/key_concepts_overview.html](https://docs.godotengine.org/en/stable/getting_started/introduction/key_concepts_overview.html)
