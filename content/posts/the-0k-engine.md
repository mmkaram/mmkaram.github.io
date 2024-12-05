---
title: "The 0k engine"
date: 2024-01-13
draft: false
summary: "A chess engine written in C++"
---
My attempt at a [chess engine in C++](https://github.com/mmkaram/0K-Engine). Using the [Universal Chess Interface](https://www.shredderchess.com/chess-info/features/uci-universal-chess-interface.html) (UCI) protocol and [this](https://github.com/Disservin/chess-library/tree/master) chess library by [Disservin](https://github.com/Disservin). I called it the "0K"-engine as 0K is part of my username in video games, but I think it's funny that you can read it as "an engine that is OK".

#### First attempts
When I first tried writing this I thought I'd try to write chess logic myself. Not only did I try to use classes for each pieces, which made move-generation painfully slow, but I wrote it in a way that made it way more complicated than it needed to be. Then when I found "chess-library" by Disservin and saw that the .h file was about 4k lines long, I remebered that the point of this project was to make a chess engine, not the logic, so I just the library instead.
For what concerns the actual engine, my first attempt at an evaluation function would loop through all the squares and add up all the piece values (plus or minus some value for where the pieces was (center is better for knights for example)). After an email conversation with the "chess-library" creator themselves, I found a better way to do it. You can see the diff in the github repo for this project under [src/engine.cpp@eval](https://github.com/mmkaram/0K-Engine/blob/master/src/engine.cpp#L23). 

#### Estimated Rating
Probably like, 700. Maybe worse

#### What I learned
I have another ongoing project, [SquashAI](/posts/squashai), where I was going to use a deep learning algorithm to teach the program what a good shot/play was. Chess programming introduced me to evaluation functions. I think I have some ideas on how to implement those into the squash coaching program.

