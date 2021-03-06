Wurstgulasch JSON API Specs
===========================

This document intends to give a quick overview on the Wurstgulasch decentral
and (somewhat) social Microblogging API.

API Endpoints are written absolute to the root resource. In `/api/0`, the `0`
stands for the version number of the API. It will be incremented if there are
changes made that are incompatible with the previous API version.

Here's a quick overview over the API endpoints:

`/api/0/`
* `user/`
  * `login`
  * `logout`
  * `create`
* `instance/`
  * `info`
  * `plugins`
* `posts/`
  * `identity/`
    * `posts`
    * `timeline`
  * `all`
  * `create`
  * `repost`
  * `reply`
* `identity/`
  * `create`
  * `share`
  * `revoke`
  * `delete`
  * `info`
  * `change`
  * `notifications`
  * `followed/`
    * `follow`
    * `unfollow`
  * `followers`
* `machines/`
  * `notify`

0. Definitions
--------------
 
0.1 Authenticated
-----------------

A call to an API endpoint marked as "authenticated" has to
contain the HTTP header ``access_token``, which can be obtained by the endpoint
``/api/0/user/login``.

Authenticated API calls can also return an Error object with the `code`
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

Generic Errors:
* `PARAMETER_INVALID`: One or mor parameters of the request were invalid. Detailed
  information will be in the error message.

0.3 Results
-----------

A result is a JSON Object containing a success field with a boolean which
indicates whether a request has been executed correctly or not. If `success` is
not `true`, there has to be at least one error object attached.

A data field can be passed, if `success` is `true`.

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
    'data': null
}
```

0.4 Notifications
-----------------

Notification Objects look like this:

```
{
    'type':         'follow',
    'subject':      'alice@wurstgulasch.sft.mx',
    'object':       'bob@wurstgulasch.example.com',
    'data':         null
}
```
`type` can be one of:
* `follow`: `subject` now follows `object`. `data` is ignored.
* `unfollow`: `subject` does not follow `object` any more. `data` is ignored.
* `post`: `subject` has posted or reposted something. `object` is ignored,
  `data` contains the post object.
* `mention`: `subject` has mentioned `object` in the post delivered in `data`.
* `identity_deleted`: `subject` has been deleted. `object` and `data` are
  ignored.

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
* Result object with welcome package consisting of a JSON object with the following attributes:
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
* `username`: the name of the new user
* `password`: the password of the new user

Returns:
* Result object

Possible Errors:
* `USERNAME_INVALID`
* `PASSWORD_INVALID`
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

    'provide': 'Wurstgulasch',
    'version':  '0.1',

    'created':  1375497042
}

```


2.2 Supported Content Plugins
-----------------------------

    /api/0/instance/plugins

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
                    'name':     'title',
                    'desc':     'Post Title',
                    'type':     'textfield',
                    'required': false
                },
                {
                    'name':     'text',
                    'desc':     'Post Content',
                    'type':     'textarea'
                    'required': true
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
                    'name':     'image',
                    'desc':     'Image',
                    'type':     'file',
                    'required': true
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
* `identity`: Name of the identity that is queried
* `(before|after)?`: Unix Timestamp
* `count`: maximum number of posts to retrieve

Returns:
* Result object with array of Post objects.

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
* `identity`: Name of the identity that is queried
* `(before|after)?`: Unix Timestamp
* `count`: maximum number of posts to retrieve

Returns:
* Result object with array of Post objects.

Possible Errors:
* `IDENTITY_NOT_FOUND`

3.3 Get most recent public posts
--------------------------------

    /api/0/posts/all

Method: GET

Gets up to ``count`` posts from an identity  before/after a specified
timestamp

Data:
* `identity`: Name of the identity that is queried
* `(before|after)?`: Unix Timestamp
* `count`: maximum number of posts to be retrieved.

Returns:
* Result object with array of Post objects.

Possible Errors:
* `IDENTITY_NOT_FOUND`

3.4 Get Complete Discussion
---------------------------

    /api/0/posts/discussion/<post_id>

Method: GET

Gets Discussion about ``post_id``. This includes replies and reposts as well 
as replies to reposts.

Returns:
* Result object with array of Post objects.

Possible Errors:
* `POST_NOT_FOUND`

3.5 Reply to post (authenticated)
---------------------------------

    /api/0/posts/reply

Method: POST

Data:
* `identity`: ``identity_id`` of the identity that should create the reply
* `content_type`: string identifying the type of content
* `original_post`: `id` field of the referenced post.
* all the fields that the `content_type` plugin requires.

Returns:
* Result object

Possible Errors:
* `POST_NOT_FOUND`
* `IDENTITY_NOT_FOUND`
* `IDENTITY_NOT_ALLOWED`
* `CONTENT_TYPE_UNSUPPORTED`
* `CONTENT_ERROR`

3.6 Create Post (authenticated)
-------------------------------

    /api/0/posts/create

Method: POST

Data:
* `identity`: ``identity_id`` of the identity that should create the post
* `content_type`: string identifying the type of content
* all the fields that the `content_type` plugin requires.

Returns:
* Result object

Possible Errors:
* `IDENTITY_NOT_FOUND`
* `IDENTITY_NOT_ALLOWED`
* `CONTENT_TYPE_UNSUPPORTED`
* `CONTENT_ERROR`

3.7 Repost (authenticated)
--------------------------

    /api/posts/repost

Method: POST

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
* `displayname`, `tagline` and `bio` are free-text fields.
* the `avatar_url` points to the identity's avatar.

4.1 Create new identity (authenticated)
---------------------------------------

    /api/0/identity/create

Method: POST

Create a new Identity.

Data:
* `displat_name`: name of the identity
* `tagline`: tagline of the identity
* `bio`: bio for the new identity
* `avatar`: File to use as an avatar, will be cropped to quadratic dimensions.

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
* `managing_identity`: the identity whose owner should be granted access

Returns:
* Result Object

Possible Errors:
* `MANAGING_IDENTITY_NOT_FOUND`
* `SHARED_IDENTITY_NOT_FOUND`
* `NOT_ALLOWED`

4.3 Revoke access to an Identity (authenticated)
------------------------------------------------

    /api/0/identity/revoke

Method: POST

Data:
* `shared_identity`: the identity to which access should be revoked
* `managing_identity`: the identity whose owner's access should be revoked.

Returns:
* Result Object

Possible Errors:
* `SHARED_IDENTITY_NOT_FOUND`
* `MANAGING_IDENTITY_NOT_FOUND`
* `NOT_ALLOWED`


4.4 List managing Identities (authenticated)
--------------------------------------------

    /api/0/identity/list_managing

Method: GET

Data:
* `identity`: Identity whose managing Identities should be listed

Returns:
* Result Object with list of Identity Objects attached.

Possible Errors:
* `SHARED_IDENTITY_NOT_FOUND`
* `NOT_ALLOWED`

4.5 Delete an Identity (authenticated)
--------------------------------------

    /api/0/identity/delete
    
Method: DELETE

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
* Result object with Identity object attached

Possible Errors:
* `IDENTITY_NOT_FOUND`


4.7 Change an Identity's Profile (authenticated)
------------------------------------------------

    /api/0/identity/change

Method: POST

Change an Identity's profile.

Data:
* `display_name`: Displayed name of the identity
* `tagline`: tagline of the identity
* `bio`: bio for the identity
* `avatar`: new avatar for the identity

Returns:
* Result object

Possible Errors:
* `IDENTITY_NOT_FOUND`
* `NOT_ALLOWED`


4.8 Get Notifications for Identity (Authenticated)
--------------------------------------------------

    /api/0/identity/notifications

Method: GET

Get Notification bjects for an Identity.

Data:
* `identity`: Handle of the identity for which the notifications should be
  fetched
* `(before|after)?`: Unix timestamp
* `count`: maximum number of Notification objects to retrieve

Returns:
* Result object with Notification objects attached

Possible Errors:
* `IDENTITY_NOT_FOUND`
* `IDENTITY_NOT_ALLOWED`

4.9 Follow someone with an identity (Authenticated)
---------------------------------------------------

    /api/0/identity/followed/add

Method: POST

Add a friend to an identity

Data:
* `user_identity`: Identity handle to add the friend to
* `friend_identity`: Identity handle of the identity to
  follow

Returns:
* Result object

Possible Errors:
* `USER_IDENTITY_NOT_FOUND`
* `FRIEND_IDENTITY_NOT_FOUND`
* `NOT_ALLOWED`

4.10 Unfollow someone when an identity (authenticated)
-----------------------------------------------------

    /api/0/identity/followed/remove

Method: DELETE

Add a friend to an identity

Data:
* `user_identity`: Identity handle that should unfollow
* `friend_identity`: Identity handle of the friend unfollow

Returns:
* Result object

Possible Errors:
* `USER_IDENTITY_NOT_FOUND`
* `FRIEND_IDENTITY_NOT_FOUND`
* `NOT_ALLOWED`
* `FRIEND_IDENTITY_NOT_FOLLOWED`

4.11 Get List of followed Identities (authenticated)
----------------------------------------------------

    /api/0/identity/followed
    
Method: GET

Get list of Identity objects followed by an identity

Data:
* `identity`: Identity handle of the Identity to query

Returns:
* Result object with array of Identity objects attached

Possible Errors:
* `IDENTITY_NOT_FOUND`
* `NOT_ALLOWED`

4.12 Get List of followers (authenticated)
------------------------------------------

    /api/0/identity/followers
    
Method: GET

Get list of Identity objects that follow an identity

Data:
* `identity`: Identity handle of the Identity to query

Returns:
* Result object with array of Identity objects attached

Possible Errors:
* `IDENTITY_NOT_FOUND`
* `NOT_ALLOWED`


5. Server-to-Server Communication
---------------------------------

Server-to-Server communication is largely done by Servers `POST`ing 
notification objects to each other.

**Security Warning**: It is strongly advised to carefully monitor and/or limit
the rate of server-to-server communication. If you're an API Provider operator
you might run into spam problems.

It's probably a good idea to pool connections to these endpoints.

5.1 Notify the server
---------------------

    /api/0/notify

Method: POST

Notify the Wurstgulasch instance about things that happened. When delivering
this endpoint, make sure to keep a backlog of failed transactions and repeat
them in a reasonable interval.

Data:
* `messages`: JSON string containing array of `Notification` objects

Returns:
* Result object
