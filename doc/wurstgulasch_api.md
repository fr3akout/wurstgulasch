Wurstgulasch JSON API Specs
===========================

This document intends to give a quick overview on the Wurstgulasch decentral
and (somewhat) social Microblogging API.

0. Definitions
--------------
 
0.1 Authenticated
-----------------

A call to an API endpoint marked as "authenticated" has to
contain the HTTP header ``access_token``, which can be obtained by the endpoint
``/api/0/user/login``.

Authenticated API cals can also return an Error object with the `code`
`INVALID_ACCESS_TOKEN`

0.2 Errors
----------

Errors are JSON objects containing an error code and a textual description of the
error that has occurred.

```
{
    'errorcode':'SHIT_HAPPENS',
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
                'errorcode':'WELL_SHIT',
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

Possible Errors:
* `INVALID_LOGIN`


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

Possible Errors:
* `REGISTRATION_CLOSED`
* `USERNAME_TAKEN`

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
    'instance': 'wurstgulasch.sft.mx',
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

Possible Errors:
* `IDENTITY_NOT_FOUND`
* `NOT_ALLOWED`

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

Possible Errors:
* `IDENTITY_NOT_FOUND`

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
* an empty array if there are no posts at all.

3.4 Get Complete Discussion
---------------------------

    /api/0/posts/discussion/<post_id>

Method: GET

Gets Discussion about ``post_id``. This includes reactions and reposts as well 
as reactions to reposts.

Returns:
* Full tree of discussion about ``post_id``, which is also the root element or
* Error object

Possible Errors:
* `POST_NOT_FOUND`

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

Possible Errors:
* `IDENTITY_NOT_FOUND`
* `IDENTITY_NOT_ALLOWED`
* `CONTENT_TYPE_MISSING`
* `CONTENT_ERROR`

3.5 Repost (authenticated)
--------------------------

    /api/posts/repost

Data:
* `identity`: `identity_id` of the identity that should repost
* `post_id`: `id` of the post to repost

Returns:
* Result Object

Possible Errors:
* `IDENTITY_NOT_FOUND`
* `IDENTITY_NOT_ALLOWED`
* `POST_NOT_FOUND`


4. Identities
-------------

Identities are roles assigned to one or more users. Users can choose
to have multiple Identities, and one identity can be managed by one or more
users. The Owner of an identity is not disclosed.

An Identity Object looks like this:

```
{
    'handle':       'toplel@wurstgulasch.sft.mx'
    'displayname':  'Top Lel'
    'tagline':      'Only catcontent.'
    'bio':          'I am only a test user.'
    'avatar_url':   'https://wurstgulasch.sft.mx/assets/13371337133742.png'
}

```

where:
* `handle` is the identity's globally unique handle. It consists of a username
  that is unique per instance and the instance's domain name separated by an 
  `@`. The username is limited to 128 characters.
* `displayname`, `taglines` and `bio` are free-text fields.
* the `avatar_url` points to the identitie's avatar.

4.1 Create new identity (authenticated)
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

Possible Errors:
* `IDENTITY_TAKEN`

4.2 Grant access to an Identity (authenticated)
-----------------------------------------------

    /api/0/identity/share

Method: POST

Data:
* `shared_identity`: the identity to which access is being granted
* `managing_identity`: the identititie whose owner should be granted access

Returns:
* a `Result` Object

Possible Errors:
* `MANAGING_IDENTITY_NOT_FOUND`
* `SHARED_IDENTITY_NOT_FOUND`
* `NOT_ALLOWED`

4.3 List managing Identities (authenticated)
--------------------------------------------

    /api/0/identity/list_managing

Method: GET

Data:
* `identity`: Identity whose managing Identities should be listed

Returns:
* A list of `Identity` Objects

Possible Errors:
* `SHARED_IDENTITY_NOT_FOUND`
* `MANAGING_IDENTITY_NOT_FOUND`
* `NOT_ALLOWED`

4.4 Revoke access to an Identity (authenticated)
------------------------------------------------

    /api/0/identity/revoke

Method: POST

Data:
* `shared_identity`: the identity to which access should be revoked
* `managing_identity`: the identity whose owner's access should be revoked.

Possible Errors:
* `SHARED_IDENTITY_NOT_FOUND`
* `MANAGING_IDENTITY_NOT_FOUND`
* `NOT_ALLOWED`

4.5 Delete an Identity (authenticated)
--------------------------------------

    /api/0/identity/delete

Data:
* `identity`: The Identity that should be deleted

Returns:
* `Result` Object

Possible Errors:
* `IDENTITY_NOT_FOUND`
* `NOT_ALLOWED`

4.6 Get Identity information
----------------------------

    /api/0/identity/info

Method: GET

Data:
* `identity`: Handle of the identity that should be queried

Returns:
* Identity Object or Error Object.

Possible Errors:
* `IDENTITY_NOT_FOUND`


4.7 Change an Identity's Profile (authenticated)
------------------------------------------------

    /api/0/identity/change

Method: POST

Change an Identity's profile.

Data:
* `name`: name of the identity
* `tagline`: tagline of the identity
* `bio`: bio for the identity
* `avatar`: new avatar for the identity

Returns:
* Result object

Possible Errors:
* `IDENTITY_NOT_FOUND`
* `NOT_ALLOWED`


4.8 Add a friend to an identity (Authenticated)
-----------------------------------------------

    /api/0/identity/friends/add

Method: POST

Add a friend to an identity

Data:
* `user_identity`: Identity handle to add the friend to
* `friend_identity`: Identity handle of the friend to add

Returns:
* Result object

Possible Errors:
* `USER_IDENTITY_NOT_FOUND`
* `FRIEND_IDENTITY_NOT_FOUND`
* `NOT_ALLOWED`

4.9 Remove a friend from an Identity (authenticated)
----------------------------------------------------

    /api/0/identity/friends/remove

Method: POST

Add a friend to an identity

Data:
* `user_identity`: Identity handle to remove the friend from
* `friend_identity`: Identity handle of the friend to remove

Returns:
* Result object

Possible Errors:
* `USER_IDENTITY_NOT_FOUND`
* `FRIEND_IDENTITY_NOT_FOUND`
* `NOT_ALLOWED`
* `FRIEND_IDENTITY_NOT_IN_FRIENDS`
