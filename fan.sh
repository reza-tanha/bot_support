#!/bin/sh

fandogh image init --name insta-bot
fandogh image publish --version 1.0
fandogh service apply -f fandogh_.yml


