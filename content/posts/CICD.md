---
title: "Deploying my own server with CI/CD and Docker"
date: 2025-03-24
draft: false
summary: "How I went about setting up a VPS to run my web app"
---

# Introduction
I'm getting really close to deploying my B2C automous squash coaching app [SquashAI](/projects/squashai). For it to trully be busniess to consumer though, I needed a way for users to upload their videos so they can be queued for analysis. After watching enough of [theo's](https://www.youtube.com/@t3dotgg) I was convinced to use NextJS with it's fancy app router and SSR, even if I had very little exprience with javascript, much less typescript and tsx. When it came to deploying, the natural choice wast ercel, which was actually one of the easiest "technical" things I've ever set up in my life. It was as simple as linking my github account, picking the repository that contained my NextJS application, and uploading my `.env.local`.

Vercel did it's magic, and I was a happy camper, being able to test my UI with it's automatic deployments and nice UI. The problems started to show after I had to start implementing the actual analysis part of the app (you know, the important part).

Vercel only lets users upload [4.5mb](https://github.com/payloadcms/payload/discussions/7569) in a single request. And given that video files can be quite large, this wouldn't fly. Problem was, most other providers had a limitation like this (this could possibly be because they're all AWS wrappers and that's the upload limit for AWS lambda). So I had to look elsewhere for a solution. This brought me to some of the most fun I've had in a while, the VPS!

After watching [this video](https://www.youtube.com/watch?v=F-9KWQByeU0&t=1110s) by Dreams of Code, I was inspired to get spin up a VPS and see how far I could get trying to replicate these platofrms as a service services like Vercel, railway.com, and netlify.

Inspired by the video, I decided to make my own requirements for this VPS system to be considered production ready.

Requirements:
    - Is publicly available on the internet
    - Automatically deploys new versions of my application when they're pushed to prod
    - Be reproduicble (this was inspired by my year long usage of [NixOS](/posts/nixos))
    - High availability, even when new versions are being deployed.
    - Be as secure as I could reasonably make it

With my needs laid out, it was time to start building.

## Automatic Deployment and Testing (CI/CD)

### Setup

Before I can begin explaining how I made this app open to my many users on the internet, I should probably explain how my project is set up.

All of the code for this bad boy to run is contained in two repos:
    - NextJS site
    - Flask API server

Each one of these had to have it's own `Dockerfile` written so that I could build them and have the VPS pull them down to maintain reproducibility.

Here's what the `Dockerfile` for the NextJS application looks like:
```docker
FROM node:20-alpine AS builder
WORKDIR /app
COPY . .
RUN rm -rf .next/
RUN npm i
RUN npm run build
RUN npx prisma generate

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json .
COPY --from=builder /app/package-lock.json .
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/prisma ./prisma
COPY --from=builder /app/app ./app
COPY --from=builder /app/next.config.ts ./next.config.ts
ENV NODE_OPTIONS="--max-old-space-size=8192"
RUN npx next telemetry disable
EXPOSE 3000
CMD ["npm", "start"]
```

The one for the flask server is similar from a high level perspective. It also contains a build step and a run step, just with a different toolchain to accomadate the different language. Both of these repos then needed a github action yaml file, located in the `./.github/workflows/` directory to install dependencies, run tests, then build those containers and push them to the GitHub container registry. This yaml file can get quite long, so I've linked the workflow for the NextJS project [here](https://gist.github.com/mmkaram/fc77b5c6bf3269b9d20dd9bdd62c8afd).

Ok, so I can build containerized versions of my repos and push them to a container registry, but how do I get that on the VPS without having to manually ssh into the box and tell docker to pull new containers? Well, Mahdy, that's a great question! This brings us to the glue that holds this system together: Docker Compose.

### VPS CI/CD

With docker compose, I can specify which containers I need to be pulled down, configure them, specifiy enviorment variables, and define how they should interact with each other. Then, then `docker compose up` command does most of the heavy lifting for me! To set up automatic deployments, I used the [watchtower](https://containrrr.dev/watchtower/) container to check for new versions of my two project containers every 30 seconds and pull down new versions if new ones are detected. Additonally, I also configured it to restart my containers one at a time, by specifying the `--rolling-restart` flag. Here's the full watchtower setup in my `compose.yml`:
```yml
  watchtower:
    image: containrrr/watchtower
    command:
      - "--label-enable"
      - "--interval"
      - "30"
      - "--rolling-restart"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```
And set these labels to both the NextJS and flask containers:
```yml
    labels:
      - "com.centurylinklabs.watchtower.enable=true"
```

That's one requirement done! To have high availability, I set the `deploy` arguments in the `compose.yml` as follows for both containers as well:
```yml
    deploy:
      mode: replicated
      replicas: 2
```
