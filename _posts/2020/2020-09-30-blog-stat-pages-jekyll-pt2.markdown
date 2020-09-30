---
layout: post
author: Taylor Talkington
title: "Creating Blog Statistic/Summary Pages with Jekyll - II"
date: 2020-09-30 07:30 -0400
tags: jekyll data!
---

Building on [the list of brews by style page I built for the brewlog]({% link _posts/2020/2020-09-18-blog-stat-pages-jekyll.markdown %}), I also wanted a page to summarize all of the ingredients I've used, with total weights.

Not just fun trivia, but this is actually useful. It could help me understand which speciality grains would be worth buying in bulk, since I'd use them enough to justify it.

Unfortunately, this isn't quite as easy as the [styles page](/brewlog/styles). In addition to creating a list of ingredients, I also need to tally up the total amount for each. And, unlike the styles, each recipe has lists of ingredients so some nested loops are needed.

This is a bit more than what can be done in markdown and Liquid.

## Jekyll Plugins
A custom plugin can be included in a Jekyll site by placing it in the _plugins directory. My plugin is a simple Ruby script: ingredients.rb. No other changes are needed to load the file, when Jekyll generates the site, it will automatically find the file and load it as a plugin.

## A Ruby Plugin
The structure of a Jekyll plugin written in Ruby is simple. I want to add a couple of filters that can be used in markdown with Liquid:

{% highlight Ruby %}
module Jekyll
  module IngredientsFilters
    # functions to define new filters
    # the function name will be the name of the new filter
  end
end

Liquid::Template.register_filter(Jekyll:IngredientsFilters)
{% endhighlight %}

I decided the easiest approach was to break the task apart into a few steps:
 - Get a list of ingredients across all recipes
 - Get a total weight for a given ingredient
 - Parse weight strings from the formatted value in the recipe
 - Format a raw weight back to a nice formatted string
 
### Ingredients List
First, generating a list of all ingredients. I actually split everything between 'grains' (mash) and 'boil.' Not only is that a logical split (between grain and hops), but the recipe definied in the front matter of each posts defines them the same way; two lists.

So, this is the filter that returns a table of grain names and corresponding total amounts. It takes a list of posts as an argument:

{% highlight Ruby %}
def grain_weights(posts)
  grains = {}
  posts.each do |post|
    post['recipe']['fermentables'].each do |grain|
      if not grains.include?(grain['name'])
        grains[grain['name']] = 0
      end
      grains[grain['name']] += parse_weight(grain['amount'])
    end
  end
  return (grains.sort_by { |name, amount| amount }).reverse
end
{% endhighlight %}

In my new page, ingredients.markdown, I use this like a normal filter: 

{% highlight liquid %}{%raw%}
{% assign grains = site.posts | grain_weights %}
{% endraw %}{%endhighlight %}

Creating a list in markdown is now super simple:

{% highlight liquid %}
{% raw %}
{% for grain in grains %}
 - {{ grain[0] }}: {{ grain[1] | format_weight -}}
{% endfor %}
{% endraw %}
{% endhighlight%}

The table can be accessed like an array, the ingredient name ends up in index '0' and the amount in '1.'

### Parsing and Formatting Weight Strings
The `grain_weights` filter uses another function, `parse_weight` to convert the string defined in the recipe to an actual number. This is done with a few simple regular expressions:

{% highlight Ruby %}
def parse_weight(amount)
  lb = amount.match /(?<lbs>[0-9\.]+) lb/
  oz = amount.match /(?<oz>[0-9\.]+) oz/
  lbs = 0
  if lb
    lbs += lb[:lbs].to_f
  end
  if oz
    lbs += oz[:oz].to_f / 16.0
  end
  return lbs
end
{% endhighlight %}

Then a simple filter to format the totals back when displaying them:

{% highlight ruby %}
def format_weight(amount)
  lbs = amount.floor
  oz = (amount - amount.floor) * 16.0
  w = ""
  if lbs > 0
    w += "%0.0f lbs" % [lbs]
  end
  if oz > 0
    if lbs > 0
      w += " "
    end
    w += "%0.1f oz" % [oz]
  end
  return w
end
{% endhighlight %}
