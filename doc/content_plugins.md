Wurstgulasch Content Plugins
============================

This document talks about how content plugins interact with the API provider
they're built for. Since there are no Wurstgulasch API providers at this time,
this document is kept very generic and more technical advice is left out on
purpose. If you have technical question about writing plugins, please refer
to the API Provider's documentation.

0. Definitions
--------------

(reserved)

1. How it works
---------------

Wurstgulasch content is managed by content plugins. Content plugins interact
with the software providing the API and make recommendations on how their
data should be presented.

A few plugins will be chosen to be canonical by the Wurstgulasch project and
should be implemented in every wurstgulasch client application and service
provider.

Other, optional content plugins can be supported optionally. Remember: It's
all about respecting the user's freedom, so it might be a good chance to 
contribute to existing plugins rather than creating new ones that do the
same thing, but a bit differently.

2. Plugins from a plugin developer's point of view
--------------------------------------------------

So you want to write, say, a microblogging plugin that differs from the
Free-text markdown plugin by the fact that it allows 140 characters per
tweet.

Let's not talk about why this is a bad idea but about how to build a plugin
like that.

Let's start. First of all, you need to write a definition object in JSON
to let the application know what's going to hit it. Definition objects 
look like this (Don't worry, we're going to talk about the details in a bit.

```
{
    'name':     'microblog',
    'version':  '0.1',
    'author':   'John Doe <john.doe@example.com>',
    'input_fields':
        [
            {
                'name':     'text',
                'desc':     'Microblog Entry',
                'type':     'textfield',
                'required': true
            }
        [
}
```

Yeah, that's it. So what do the fields actually mean?

* `name` is obviously the name of your content plugin
* `version` is the version that is installed on the API provider.
* `author` is the name and the email address of you, the author. But why 
  give the email address? Tough one, but it really makes sense to be 
  reachable in case of bugs and/or security problems with your plugins.
* `input_fields`: is an array of the input fields you advise the application
  programmer to show to your user if said user wishes to create a content
  object with your plugin.

Input fields, themselves, are simple JSON objects with the following
values:

* `name`: the name of the field, and the name of the POST parameter you
  are going to get from the application on content object creation.
* `desc`: a string that describes what the user should put in your field.
* `type`: can be one of `textfield`, `textarea` or `file`. Use `textfield` for
  short texts, `textarea` for long texts and `file` obviously for files.

Let's talk about versioning for a bit. In order for applications to be able
to manage plugins in an efficient manner, you should stick to the semantic
versioning scheme. You can find it on http://semver.org

Alright. So all we have left to do then is to make some content objects. At
it's heart, Wurstgulasch is driven by content objects. You should be very
selective in what you need to save to the API provider's database or to disk
in order to keep disk usage low and transfer fast. Please keep in mind that
plugins, again, drive Wurstgulasch and the user experience can be spoiled
completely by a single plugin.

So, what does a content object look like, then? Essentially, they're JSON
objects and their attributes might correlate to the `input_fields` array from
your definition.

Now you really should write some documentation about how you would like your
content to look like on the screen. That facilitates application development
a great deal.


2. Plugins from an application developer's point of view
--------------------------------------------------------

As an application developer, your job is to provide users with a comfortable
way to access and create content on Wurstgulasch. So, let's take a look how
your software is interacting with plugins.

2.1 Posting
-----------

If you want to create a post for a user, you are going to use the `posts/create`
endpoint. The most critical thing to know here is which data to pass to the
API provider at that point.

Let's review the API call. The two things that have to be in every
`post/create` API call are `identity` and `content_type` where `identity` is -
of course the `identity_id` if the identity you want to post with and
`content_type` is the name of the plugin that should handle the plugin.

The other fields are determined by the plugin's definition. Pass everything as
strings, even if you only let the user enter Integers.

If the plugin finds anything wrong with the values you sent, it will return a
result object with errors attached to it.

2.2 Displaying Posts
--------------------

As an application developer you really should read through the recommendations
from the plugin developer. But then again, it's your choice.

If you come across a `content_type` that you don't recognize, you can either
display a message or try to find a generic way of displaying input.


3. Plugins from an API provider developer's point of view
---------------------------------------------------------

As an API provider developer, you have the task to facilitate plugin
development. So please keep your API free from unnecessary boilerplate code
or obscure idioms so plugin developer's can go about their business without
having to worry about your internals.

Plugins have the following duties in your infrastructure:

* They expose themselves with their definition files
* They handle content creation and
* They handle content replication

For example, let's think in terms of the above microblogging plugin. The API
gets a POST request, with the following fields:
* `identity` which is `john.doe@wurstgulasch.example.com`
* `content_type` which in this case is `microblog`
* and the plugin's only field, `text`.

So, from the `content_type`, you can tell, that it's time to invoke the
`microblog` plugin in the way that you specified.

Now, the plugin works it's magic and gives you back - again, in the way you
specified - a content object that you might store in your database or on disk.

For more complex content types that involve larger amounts of data, you should
provide plugin developers with facilties to create files on disk (for security
reason it might be best to not let plugin developers choose their own path but
just give them a method to store something and return the path) to the plugin.

If the plugin encounters an error, you should return a result object with a
`CONTENT_PROBLEM` error in it. 
