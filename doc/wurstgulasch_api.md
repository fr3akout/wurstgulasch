Wurstgulasch JSON API Specs
===========================

0. Definitions
--------------

Authenticated: A call to an API endpoint marked as "authenticated" has to
contain the HTTP header "access\_token", which can be obtained by the endpoint
``/api/0/login``.

1. Basic User Interaction
-------------------------

1.1 Login
---------

    /api/0/login

Authentifies a User against a Wurstgulasch Instance

Data:
    * username
    * password

Result:
    * success
    * access\_token
    * valid\_until

1.2 Logout (authenticated)
--------------------------

    /api/0/logout

Terminates a session and invalidates the access\_token passed in the header.

Data:
    (None)

Result:
    * success (boolean)


2. Instance Information
-----------------------

2.1 Instance Info
-----------------

    /api/0/instance/info

Gets Information about the queried instance

2.2 Supported Content Plugins
-----------------------------

    /api/0/instance/supported_content_plugins

Gets List of content Plugins the Instance supports.

3. Posts
--------

3.1 Get Identity Timeline (authenticated)
-----------------------------------------

    /api/0/posts/identity/timeline

Gets up to <count> posts from an identity timeline before/after a specified
timestamp

Data:
    * identity: Name of the identity that is queried
    * (befor|after)?: Unix Timestamp

Result:
    * Array of post objects


3.2 Get Identity Posts
----------------------

    /api/0/posts/identity/posts

Gets up to <count> posts from an identity  before/after a specified
timestamp

Data:
    * identity: Name of the identity that is queried
    * (befor|after)?: Unix Timestamp

Result:
    * Array of post objects


3.3 Get most recent public posts
--------------------------------

    /api/0/posts/all

Gets up to <count> posts from an identity  before/after a specified
timestamp

Data:
    * identity: Name of the identity that is queried
    * (befor|after)?: Unix Timestamp

Result:
    * Array of post objects


3.4 Get Complete Discussion
---------------------------

    /api/0/posts/discussion/<post_id>

Gets Discussion about <post_id>. This includes reactions and reposts as well 
as reactions to reposts.

Data:
    (none)

Result:
    * Full tree of discussion about ``post_id``. root element is the
      referenced post.
