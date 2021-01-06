---
layout: post
author: Taylor Talkington
title: Converting a TFVC repository history to Git
date: 2021-01-06 07:30 -0500
---

## Good News, Bad News

One of my projects at work uses Team Foundataion Server (TFVC) for version control. We were required to use that instead of git when we were first implementing versioning control.

So, the good news: we will be required to transition to git soon.

The bad news: only the last 180 days of commits can be converted, at most.

Instead of losing the majority of our commit history I wrote a small script to step through each change in TFVC, check those changes into git and create backdated commits.

It's not fast, but it works!

## Requirements

Doing this requires two things to be installed:
 - Visual Studio (for the Team Foundataion Server command line tools)
 - Git for Windows

And, you need the TFVC repository mapped and downloaded to a local directory.

## Initial setup

Before running the script, setup a new git repository.

Run git bash and get to the directory of the mapped branch to convert. Initialize the git repo and then add a .gitinore file that contains the names of any files/folders that aren't mapped to TFS but exist in the local folder. Then add it as a local commit

{% highlight terminal %}
$ git init
...
$ git add .gitignore
...
$ git commit -m "Initial commit (start of TFVC conversion)"
..
{% endhighlight %}

At this point, you have a new master branch...it's a good time to rename it:

{% highlight terminal %}
$ git branch -m master working
{% endhighlight %}

## The script

Now, run the following script from the git bash prompt while in the newly created git repo.

{% highlight bash %}
#!/bin/bash


# You must change your date format options in windows (right click on the clock on system bar)!
# The TF utility is idiotic and uses those formats to display the date, and default settings
# results in a date that CAN NOT be parsed by standar libraries!
# the git commit --date format uses strftime format options.
# The tf utility outputs the date using 'Long Date' followed by 'Long Time' formats.
# These seem to work well:
# Long date: MMMMM dd, yyyy
# Long time: HH:mm:ss

# Open Developer Command Prompt and run `where tf`
TF="C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\IDE\CommonExtensions\Microsoft\TeamFoundation\Team Explorer\TF.exe"

VERSIONS=`"$TF" hist -noprompt -recursive -sort:ascending . | awk 'NR > 2 {print $1}'`

for VERSION in $VERSIONS
do
    COMMENT=`"$TF" hist -noprompt -recursive -version:$VERSION -format:detailed . | grep -m 1 -A 1 "Comment:" | awk 'NR > 1 {sub(/^[ \t]+/, ""); print $0}'`
    DATE=`"$TF" hist -noprompt -recursive -version:$VERSION -format:detailed . | grep -m 1 "Date:" | sed "s/Date: //g"`
    echo "Version $VERSION @ $DATE -> $COMMENT"
    echo "Getting TFVC..."
    "$TF" get -recursive -version:$VERSION > /dev/null
    echo "Commiting to git..."
    git add * > /dev/null
    git commit -a --date="$DATE" -m "$COMMENT" > /dev/null
done
{% endhighlight %}

## Piece by piece

{% highlight bash %}
# Open Developer Command Prompt and run `where tf`
TF="C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\IDE\CommonExtensions\Microsoft\TeamFoundation\Team Explorer\TF.exe"
{% endhighlight %}

This is the TFS command line utility. As the comment states, open up a Visual Studio developer command prompt and run `where tf` to get the path.

{% highlight bash %}
VERSIONS=`"$TF" hist -noprompt -recursive -sort:ascending . | awk 'NR > 2 {print $1}'`
{% endhighlight %}

This gets all of the changeset IDs for the current branch, including those for all files and folders contained in the branch (`-recursive`), outputs it to stdout (`-noprompt`), and sorts by earliest commit first (`-sort:ascending`).

Out of all of the info printed out, we only want the first column of values (` {print $1}`) and only after the first two lines (which is a banner and column headers) have been printed (`NR > 2`).

{% highlight bash %}
for VERSION in $VERSIONS
do
{% endhighlight %}

`VERSIONS` is now a list of changeset ids, so we will loop over them, one by one.

{% highlight bash %}
COMMENT=`"$TF" hist -noprompt -recursive -version:$VERSION -format:detailed . | grep -m 1 -A 1 "Comment:" | awk 'NR > 1 {sub(/^[ \t]+/, ""); print $0}'`
{% endhighlight %}

Get all the details for this changeset, and grab the comment from it. We need the `-format:detailed` because the comment can be truncated otherwise.

Changesets that are children of other changesets will display multiple comments and dates. We only want the first one (`grep -m 1`) and the comment is actually on the line after the word 'Comment:' (` -A 1 "Comment:"`). 

In addition, we don't want the leading tab on the comment, so remove it (`awk 'NR > 1 {sub/^[ \t]+/, ""); print $0}'`).

{% highlight bash %}
DATE=`"$TF" hist -noprompt -recursive -version:$VERSION -format:detailed . | grep -m 1 "Date:" | sed "s/Date: //g"`
{% endhighlight %}

Pretty much the same as the above, but this time get the date of the changeset.

{% highlight bash %}
"$TF" get -recursive -version:$VERSION > /dev/null
{% endhighlight %}

Get all of the files for this changeset.

{% highlight bash %}
git add * > /dev/null
git commit -a --date="$DATE" -m "$COMMENT" > /dev/null
{% endhighlight %}

Add the changes and commit them. Both `git add *` and `git commit -a` are used because `git commit -a` won't pickup untracked changes and `git add *` won't pickup deleted files.

## Notes

Note, this is fairly simple:
 - It uses the current user as the author and commiter
 - Only the first line of the comment is used
 - It's not smart about what's changed each time...it just adds everything. There's almost certainly some edge cases that would break it.

