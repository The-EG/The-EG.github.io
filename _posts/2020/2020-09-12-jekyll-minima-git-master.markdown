---
layout: post
author: Taylor Talkington
title: "Updating Jekyll To Use The Minima Theme From Git Master"
date: 2020-09-13 08:40:00 -0400
tags: jekyll themes
---
While setting up this blog I was trying to find a good theme to use. I like the minima theme, the default one that comes with a new Jekyll project, but I wanted a dark color scheme and I didn't really want to manually customize the styling.

# v3.0
After trying a few themes that either didn't work, or I didn't like, I finally conceded to the fact that I'd just have to customize minima for what I wanted.

I headed over to the [git page](https://github.com/jekyll/minima) to see how I needed to do it...and look!

>  Skins  
>  Minima 3.0 supports defining and switching between multiple color-palettes (or skins).

Just what I need! Except...I don't have version 3.0. It took me a bit to figure out, that's because it hasn't been released yet. If you are using a Gem to get minima, you have version 2.5.1.

I needed the version from git, but I didn't want to manually copy everything over, I still want it to be used as a Gem.

Thankfully, a [comment on an issue](https://github.com/jekyll/minima/issues/411#issuecomment-643825456) explains how to do just that. Change the minima reference in the Gemfile:

{% highlight ruby %}
#gem "minima"
gem "minima", :github => 'jekyll/minima' # not specifying a commit, I just want master
{% endhighlight %}

After that, I use bundle to update everything to pull it in:

{% highlight console %}
PS E:\dev\the-eg.gitlab.io> bundle update
Fetching https://github.com/jekyll/minima.git
...
Using minima 2.5.0 (was 2.5.1) from https://github.com/jekyll/minima.git (at master@a98a8fe)
...
{% endhighlight %}

Notice that it says it's now 2.5.0, but it obviously did pull it from git. That's ok, the version in master hasn't been updated yet for some reason, it really is the new version.

Looking at the output of Jekyll for my site, I can see the new theme worked, but it's also missing some things. I have to fix a few things in _config.yml for v3.0:

{% highlight yaml %}
# the author field works a bit differently now
#author: Taylor Talkington
#email: "taylor.talkington@gmail.com"
author:
  name: Taylor Talkington
  email: "taylor.talkington@gmail.com"

# so do the social links and there are more available now.
# Also, I can specify the skin now!
#github_username: The-EG
minima:
  skin: dark
  date_format: "%Y-%m-%d %H:%M"
  social_links:
    github: The-EG
    linkedin: taylor-talkinton
    gitlab:
      - username: The-EG
        instance: gitlab.com
...
{% endhighlight %}

There, now it's all working again. Except, it's showing a button for a twitter acount on the main page still for @jekyllrb. If I specify a twitter account it will show that instead, but I don't have one I want to use, I just want it to not display at all.

I eventually figured out that it's displaying the twitter button because it's reading in defaults from the theme's _config.yml and it is defined there.

I don't need those defaults, since I've set everything I want in my own _config.yml, so I'll tell it to ignore the theme's file (in my _config.yml):

{% highlight yaml %}
ignore_theme_config: true
{% endhighlight %}

Now my blog is using v3.0 of the minima theme and I'm able to easily switch skins!
