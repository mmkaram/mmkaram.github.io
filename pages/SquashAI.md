This is a rudimentary explanation of the of the Squash AI program, if you want more details, contact me via [LinkedIn](https://www.linkedin.com/in/mahdy-karam).

## Introduction

What is SquashAI? Why did I make it? And why is it important?

SquashAI is a mobile application intended to help squash players improve their game. It does this by providing a way to track the player's performance and provide feedback on how to improve. It also provides a way to track the player's progress over time.

I made it because I wanted to improve my own game, and I thought that this would be a good way to do it. I also wanted to learn more about machine learning, and this seemed like a good way to do that as well.

As I progressed in the project, I realized that it could be used to help other players improve *their* game. Coaching is expensive, and this should be way cheaper to run. In addition, coaches aren't statisticians. They can't tell you how your game has changed over time with the accuracy that a computer can.

In addition, I was kinda fed up of all the other sports having stats like RBI (baseball), passing yards (american football), and PPG (basketball). We're in the Olympics now, we better act like it.

## How it works

There is one point of data collection: the video. A video can either be streamed live into the program, or it can be uploaded from the device's storage. 

Once there is a feed, the real work can begin. Three key data points are collected every frame.
1. The position of the ball
2. The positions of both players
3. The bounds of the court

## 1. Ball Tracking

Using basic computer vision techniques (KNN background detection, dilation, and more) with OpenCV, we can get the position of the ball ~90% of the time.

![Ball Tracking](/assets/images/ball_tracking.png)