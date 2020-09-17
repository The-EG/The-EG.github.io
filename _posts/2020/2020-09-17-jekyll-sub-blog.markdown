---
layout: post
author: Taylor Talkington
title: "Setting Up a 'Sub' Blog with Jekyll and GitLab"
date: 2020-09-17 17:15:00 -0400
tags: jekyll gitlab
---

Setting up this blog inspired me to create something else: a brew log for all of the beer, wine, mead and other stuff that I make.

I loved how easy it was to create a blog with Jekyll, but I wanted the brew log to be it's own 'sub' blog, with an independent configuration, theme, etc.

Luckily, the way that [GitLab generates URLs](https://docs.gitlab.com/ee/user/project/pages/getting_started_part_one.html) worked well for this: I could create a new project for my sub-blog and it would appear as a folder of this blog (perfect!).

Setting up the blog itself is easy, just go through the [normal Jekyll quick start](https://jekyllrb.com/docs/#instructions), create a project for it on GitLab and include a [GitLab CI configuration](https://about.gitlab.com/blog/2016/04/07/gitlab-pages-setup/#add-gitlab-ci).

But, Jekyll requires some configuration changes to work this way.

### BaseURL
Since the brewlog will be at `/brewlog/` and not `/`, Jekyll needs to be told to use that path, by setting it in `_config.yml`:

{% highlight yaml %}
baseurl: "/brewlog/"
{% endhighlight %}

### Links

Also any links that aren't using variables need to also include that path, such as including pictures. Instead of `/assets/<picture>.png` I use `/brewlog/assets/<picture>.png`.

I should also be able to use `{% raw %}{{ site.baseurl }}{% endraw %}` instead of specifying `/brewlog/` manually in most cases.

