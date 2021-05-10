---
layout: post
author: Taylor Talkington
title: Using Font Awesome Icons with Material-UI & React
date: 2021-05-10 11:40
---

The adventures with creating web sites with React and Material UI continue. Material UI has its own set of icons, but I find that Font Awesome still has a better selection.

There doesn't seem to be much for documentation on how to use Font Awesome within Material UI, perhaps because it is so easy.

## Installation

First, install the free version of Font Awesome:

{% highlight terminal %}
npm install '@fortawesome/fontawesome-free'
{% endhighlight %}

## Import the Stylesheet

Next, bring in the stylesheet, similar to using Font Awesome on a traditional website, and the `Icon` component from Material-UI

{% highlight javascript %}
import '@fortawesome/fontawesome-free/css/all.css';

import Icon from '@material-ui/core/Icon';
{% endhighlight %}

## Using an Icon

{% highlight javascript %}
<Icon className="fa fa-fire" />
{% endhighlight %}
