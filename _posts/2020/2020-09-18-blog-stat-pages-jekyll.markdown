---
layout: post
author: Taylor Talkington
title: "Creating Blog Statistic/Summary Pages with Jekyll"
date: 2020-09-18 15:40 -0400
tags: jekyll data!
---

Now that I have [the brewlog](/brewlog/) up and running, I wanted to do more than just make a list of brews. I thought it would be cool to some summarization; total amount of different ingredients used, different styles, and so on.

I wanted to do this within Jekyll without using addtional programs or scripts, and I wanted it utilize the data already available in the posts themselves, instead of creating yet another dataset.

## Data
Each post in the brew log has the recipe and brew information defined within the front matter of the post, in YAML.

{% highlight yaml %}
---
layout: post
title: "Taylor's CaraLager"
brew_type: beer

recipe:
  type: "All Grain"
  size: "5.25 gallon"
  style: "2B - International Amber Lager"
  fermentables: 
    - name: "2-Row (US)"
      amount: "8 lbs 12 oz"
      perc: 89.2%
    - name: "Crystal 80L"
      amount: "5 oz"
      perc: 3.2%
    - name: "Munich 20L"
      amount: "5 oz"
      perc: 3.2%
...
---
{% endhighlight %}

I originally did this so that the data was accessible from Liquid; I have an include that displays the recipe in a standard format on all posts, and updates to that format only happen in a single file.

It turns out that I can also use it to summarize the posts, too.

## Jekyll Liquid Filters
Jekyll [already provides](https://jekyllrb.com/docs/liquid/filters/) some additional Liquid filters that make this task pretty easy, namely `where_exp` and `group_by_exp`.

Creating a [style summary page](/brewlog/styles/) is actually pretty simple.

First, I group the pages up by style, but only posts for 'beer' (later I plan on separating mead and wine out into their own lists):

{% highlight liquid %}
{% raw %}
{% assign beer_styles = site.posts | where_exp: "item", "item.brew_type == 'beer'" | group_by_exp: "item", "item.recipe.style" %}
{% endraw %}
{% endhighlight %}

This:
 - takes all of the posts in the site: `site.posts`
 - filters it down to just 'beer' posts: `| where_exp: "item", "item.brew_type == 'beer'"`
 - groups the remaining posts up by the style: `| group_by_exp: "item", "item.recipe.style"`
 - assigns it to `beer_styles`: `assign beer_styles = `

`beer_styles` is now an arrary of objects with two attributes:
 - `name` - which is the name of the style (a value from `post.recipe.style`)
 - `items` - all of the posts with that value of `post.recipe.style`

Now I can loop through each style, and create a list item for each: 

{% highlight liquid %}{% raw %}
{% for style in beer_style %}
 - {{ style.name }}
 ...
{% endraw %}{% endhighlight %}

And for each list item (style), group all of the brews by name:
{% highlight liquid %}{% raw %}
...
{%- assign beer_names = style.items | group_by_exp: "item", "item.title" -%}
{%- for name in beer_names %}
   - {{ name.name }}
...
{% endraw %}{% endhighlight %}

_Then_, for each brew, display the brew date and link to the post:

{% highlight liquid %}{% raw %}
...
{%- for beer in name.items -%}
     {%if forloop.first <> true %} | {% endif %}
     [{{ beer.date | date: site.minima.date_format }}]({{ beer.url | relative_url }})
...
{% endraw %}{% endhighlight %}

The `{%raw%}{%if forloop.first <> true %} | {% endif %}{%endraw%}` part puts a `|` character between each post link. Finally, close up all of the for loops (whew!):

{% highlight liquid %}{% raw %}
{%- endfor %}
{%- endfor %} 
{%- endfor %}
{% endraw %}{% endhighlight %}

All togther:

{% highlight liquid %}{% raw %}
## Beer
{% assign beer_styles = site.posts | where_exp: "item", "item.brew_type == 'beer'" | group_by_exp: "item", "item.recipe.style" %}
{% for style in beer_styles %}
 - {{ style.name }}
{%- assign beer_names = style.items | group_by_exp: "item", "item.title" -%}
{%- for name in beer_names %}
   - {{ name.name }}
{%- for beer in name.items -%}
     {%if forloop.first <> true %} | {% endif %}
     [{{ beer.date | date: site.minima.date_format }}]({{ beer.url | relative_url }})
{%- endfor %}
{%- endfor %} 
{%- endfor %}
{% endraw %}{% endhighlight %}

A summary page in 14 lines and no custom extenions/scripts...not bad!

![styles](/assets/styles_summary.png)
