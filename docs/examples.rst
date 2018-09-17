Examples
########

Encode
======

.. code-block:: python

   >>> import characterentities as cent
   >>> cent.encode(u'Hello <strong>\U0001f310</strong>&nbsp;!')
   u'Hello &lt;strong&gt;&#x1f310;&lt;/strong&gt;&amp;nbsp;!'

   >>> cent.encode(u'Hello <strong>\U0001f310</strong>&nbsp;!', False)
   u'Hello <strong>&#x1f310;</strong>&nbsp;!'
