################
daybed-browserid
################

.. image:: https://travis-ci.org/spiral-project/daybed-browserid.png
    :target: https://travis-ci.org/spiral-project/daybed-browserid


Highlights
==========

Daybed is account agnostic. You can ask it to give you a token and
then use this token for your data.

This makes it easy to use Daybed with an existing application by
linking a token to a user.

Also if you want to use only Daybed as you full application stack, you
may want to let the user connects and get back its data.

This plugin to daybed let you connect to daybed using a BrowserID
assertion and the BrowserID protocol::


   curl -X POST /tokens/browserid -H "Authorization: BrowserID <bid_assertion>"

   {
       "credentials": {
           "algorithm": "sha256",
           "id": "15afde15e6b1a923c21769ae7187542e14fb82aead7c10a3e52ef7feca35b21a",
           "key": "698e8321da6bd99a14150f10d1130ccf45b458df007c31a5cfa9150f667f75a1"
       },
       "sessionToken": "a4330f4140b3e4e5c435de5579c28b6ca180722b080a2895ff78de92e017e1f4"
   }

You will get back a status 201 — CREATED if a new token has been
generated and a status 200 — OK if a token already existed for that account.
