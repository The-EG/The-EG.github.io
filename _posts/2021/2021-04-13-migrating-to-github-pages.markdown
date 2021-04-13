---
layout: post
author: Taylor Talkington
title: Migrating a GitLab Jekyll Site to GitHub Pages
date: 2021-04-13 13:50
---

While I'll prefer GitLab's process for hosting jekyll sites from a git repo, I already have other projects on github and it didn't make sense to have things in both anymore...so I decided to consolidate everything to github, including this blog.

## GitHub Repo

Migrating this blog itself was fairly straight forward. I had to create a new repository under my account with the appropriate name (The-EG.github.io). 

Surprisingly, just pushing my existing gitlab blog repo to a branch called 'gh-pages' was enough. As soon as I went into the github repo settings to enable pages, it was already enabled and the website was ready! No CI setup at all! 

But, the theme wasn't working properly. Also, reading through the documentation, I found that I needed to change my gemfile a bit for everything to work properly, including being able to preview the site locally:

{% highlight ruby %}
# remove jekyll itself
#gem "jekyll", "~> 4.1.1"
gem "github-pages", "~> 214", group: :jekyll_plugins
{% endhighlight %}

## Theme

So, I had my blog migrated by just pushing it to the 'gh-pages' branch of my new repo, but the theme needed to be fixed. I discovered that using custom themes with github-pages isn't quite the same as it was with gitlab. After trying a few of the 'supported' themes, I decided to just stick with Minima and customize it to my needs.

First I had to remove the Minima I was using from my gemfile:

{% highlight ruby %}
#gem "minima", :github => 'jekyll/minima'
{% endhighlight %}

After a `bundle update` my local environment was now using Minima 2.5.1 instead of 3.0. But, the local preview was still showing the dark theme that I wanted, not the default theme that github was. Somehow it was still picking up my config for 3.0, so I had to remove those from _config.yml:

{% highlight yaml %}
#author:
#  name: Taylor Talkington
#  email: "taylor.talkington@gmail.com"

author: Taylor Talkington
email: "taylor.talkington@gmail.com"

minima:
#  skin: dark
  date_format: "%Y-%m-%d %H:%M"
#  social_links:
#    twitter: 
#    github: The-EG
#    linkedin: taylor-talkington
#    facebook: tstalkington

github_username: The-EG
linkedin_username: taylor-talkington
facebook_username: tstalkington
{% endhighlight %}

At this point I also realized I was just going to customize Minima for my needs, including the layouts, so I decided to copy all of the `_layouts`, `_includes`, `_sass` folders from the minima theme files to my blog repo.

Now, the local preview matches what gets generated on github! I can continue editing `_sass/**.scss` and eventually the layouts to get a better looking blog.