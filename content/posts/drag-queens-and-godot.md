---
date: 2023-05-17
title: Drag Queens and the Godot Engine
description: who doesn't love drag?
license: commercial
draft: true
---
# Drag Queens and Godot

On my birthday this past year, I visited Drag Con here in LA. It happening on my birthday felt right. As a show Drag Race has slowly taken over my life, and I have a huge appreciation for the art of Drag. I'm also lucky to have a friend who does drag (spledidly). With House of Love cocktails to guide my friends and I, we were lucky to meet a few of our favorites while testing the limits of how intoxicated a group should be in public.

I'm using that story mostly as an excuse to share these pictures of my friends and I being drunk next to drag queens, but also to intro a drag-themed card game I've been working on, called Slay Qween.

## A Drag themed trading card game

After completing a framework-less rewrite of my website, I decided that it was time to start working on a game. And, to celebrate the timing of DragCon, I decided to make a drag themed card game in the style of Triple Triad. Triple Triad is a card battler originally from Final Fantasy VIII, but was re-tailored for Final Fantasy XIV some years later. There's also mobile and web game versions that I've seen in the wild that do and don't carry any fun likely unlicensed final fantasy IP[^1]. 

<details>
<summary>Click for a brief Triple Triad description</summary>
Two players play against one another, on a 3x3 board. Each come equipped to play with five cards of varying value. They take turns laying a card on the board. If a player lays their card to an adjacent competitors card, they battle, based on the cards values for their adjacent sides. The winner of the battle claims the other card, transforming ownership of the card to the other player. The winner of the game is the one who controls the most cards by the time the board has been filled (any unplayed cards count towards this total).
</details>
I spent some time deliberating how I would build out the game, before deciding on using the Godot Engine v4. The balance of approachability, and iteration speed with GDScript, along with the ability to compile to mobile and PC/Mac targets won me over :hugging_face.

[^1]:I'm also not making this with the queens explicit permission, though I'd like to think if I build something of interest, perhaps it's something that could get packaged and sold to serve the queens :raised_hands: :queen:.
