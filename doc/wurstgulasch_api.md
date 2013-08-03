Wurstgulasch JSON API Specs
===========================

0. Definitions
--------------
 
0.1 Authenticated
-----------------

A call to an API endpoint marked as "authenticated" has to
contain the HTTP header ``access_token``, which can be obtained by the endpoint
``/api/0/user/login``.

0.2 Errors
----------

Errors are JSON objects containing an error code and a textual description of the
error that has occurred.

```
{
    'code':     'SHIT_HAPPENS',
    'message':  'Something, somewhere went terribly wrong'
}
```

0.3 Results
-----------

A result is a JSON Object containing a success field with a boolean which
indicates whether a request has been executed correctly or not. If `success` is
not `true`, there has to be at least one error object attached.
For Example:

```
{
    'success': true
    'errors':
        [
            {
                'code':     'WELL_SHIT',
                'message':  'My hovercraft is full of eels.'
            }
        ]
}
```

1. Basic User Interaction
-------------------------

1.1 Login
---------

    /api/0/user/login

Method: POST

Authentifies a User against a Wurstgulasch Instance

Data:
* username
* password

Returns:
* A welcome package consisting of a JSON object with the following attributes:
    * `result`: Result object
    * `access_token`: 256 character string
    * `valid_until`: Integer, number of secunds the token will be valid,
      0 if valid forever.
    * `available_identities`: List of identities the user has access to


1.2 Logout (authenticated)
--------------------------

    /api/0/user/logout

Method: GET

Terminates a session and invalidates the ``access_token`` passed in the header.

Returns:
* Result object.

1.3 Create a new user account
-----------------------------

    /api/0/user/create

Method: POST

Creates a new user account.

Data:
* `username`: the name of the newuser
* `password`: the password of the new user

Returns:
* Result object

1.4 Create new identity (authenticated)
---------------------------------------

    /api/0/identity/create

Method: POST

Create a new Identity.

Data:
* `name`: name of the identity
* `tagline`: tagline of the identity
* `bio`: bio for the new identity
* `avatar`: File for 

Returns:
* Result object


2. Instance Information
-----------------------

2.1 Instance Info
-----------------


    /api/0/instance/info

Method: GET

Gets Information about the queried instance. Responses look like:

```
{
    'name':     'Wurstgulasch Instance',
    'admin':    'johannes@weltraumpflege.org',

    'software': 'Wurstgulasch',
    'version':  '0.1',

    'created':  1375497042
}

```

2.2 Supported Content Plugins
-----------------------------

    /api/0/instance/supported_content_plugins

Method: GET

Gets List of content plugins the Instance supports.

This might look something like:

```
[
    {
        'name':             'text',
        'version':          '0.1',
        'author':           'Max Mustermann'
        'input_fields':
            [
                {
                    'name': 'title',
                    'desc': 'Post Title',
                    'type': 'textfield'
                },
                {
                    'name': 'text',
                    'desc': 'Post Content',
                    'type': 'textarea'
                }
            ]
    },
    {
        'name':             'image',
        'version':          '0.1',
        'author':           'Max Mustermann'
        'input_fields':
            [
                {
                    'name': 'image',
                    'desc': 'Post Title',
                    'type': 'file'
                },
                {
                    'name': 'description',
                    'desc': 'Post Content',
                    'type': 'textarea'
                }
            ]
    }

]

```
If you are going to work with the Plugin API, please read the plugin API
specification.

3. Posts
--------

Posts are JSON objects of the following structure:

```
{
    'id':           '1337133713371337@wurstgulasch.sft.mx',
    'author':       'johannes@wurstgulasch.sft.mx',
    'timestamp':    1375497546,
    'reply_to':     null,
    'content-type': 'text',
    'content':
        {
            'title':    'Hello, World!',
            'text':     'This is my first post on Wurstgulasch'
        },
    'reposters':    []
    'replies':      []
}
```

with:
* `id` being a locally unique ID, followed by an `@` and the actual domain
  name of the wurstgulasch instance
* `author` being the globally unique wurstgulasch handle
* `timestamp` being the time of creation in seconds after January 1st 1970,
   00:00
* `reply_to` (if applicable) being the `id` of the referenced posts, `null`
  otherwise.
* `content_type` being the name of a plugin.
* `content` being an object of the specified plugin
* `reposters` being an array of globally unique wurstgulasch handles who have
  reposted this post
* `replies` an array of `Post` objects that reply to this post.


3.1 Get Identity Timeline (authenticated)
-----------------------------------------

    /api/0/posts/identity/timeline

Method: GET

Gets up to ``count`` posts from an identity timeline before/after a specified
timestamp

Data:
* identity: Name of the identity that is queried
* (befor|after)?: Unix Timestamp

Returns:
* Array of post objects or
* Error object

3.2 Get Identity Posts
----------------------

    /api/0/posts/identity/posts

Method: GET

Gets up to ``count`` posts from an identity  before/after a specified
timestamp

Data:
* identity: Name of the identity that is queried
* (befor|after)?: Unix Timestamp

Returns:
* Array of post objects or
* Error object

3.3 Get most recent public posts
--------------------------------

    /api/0/posts/all

Method: GET

Gets up to ``count`` posts from an identity  before/after a specified
timestamp

Data:
* identity: Name of the identity that is queried
* (befor|after)?: Unix Timestamp

Returns:
* Array of post objects or
* Error object

3.4 Get Complete Discussion
---------------------------

    /api/0/posts/discussion/<post_id>

Method: GET

Gets Discussion about ``post_id``. This includes reactions and reposts as well 
as reactions to reposts.

Returns:
* Full tree of discussion about ``post_id``, which is also the root element or
* Error object

3.5 Create Post (authenticated)
-------------------------------

    /api/0/posts/create

Method: POST

Data:
* `identity`: ``identity_id`` of the identity that should create the post
* `content_tupe`: string identifying the type of content
* all the fields that the `content_type` plugin requires.

Returns:
* Result object
