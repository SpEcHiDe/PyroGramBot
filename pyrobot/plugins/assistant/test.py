from pyrogram import Client, filters
from pyrogram.enums import ParseMode

@Client.on_message(
    filters.command("test")
)
async def testcomnd(_, message):
    m = """*bold \*text*
_italic \*text_
__underline__
~strikethrough~
||spoiler||
*bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold*
[inline URL](http://www.example.com/)
[inline mention of a user](tg://user?id=123456789)
![👍](tg://emoji?id=5368324170671202286)
`inline fixed-width code`
```
pre-formatted fixed-width code block
```
```python
pre-formatted fixed-width code block written in the Python programming language
```
>Block quotation started
>Block quotation continued
>Block quotation continued
>Block quotation continued
>The last line of the block quotation
**>The expandable block quotation started right after the previous block quotation
<**
>It is separated from the previous block quotation by an empty bold entity
**>Expandable block quotation continued
Hidden by default part of the expandable block quotation started
Expandable block quotation continued
The last line of the expandable block quotation with the expandability mark
<**"""
    await message.reply(m, parse_mode=ParseMode.MARKDOWN)
    h = """<b>bold</b>, <strong>bold</strong>
<i>italic</i>, <em>italic</em>
<u>underline</u>, <ins>underline</ins>
<s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
<span class="tg-spoiler">spoiler</span>, <tg-spoiler>spoiler</tg-spoiler>
<b>bold <i>italic bold <s>italic bold strikethrough <span class="tg-spoiler">italic bold strikethrough spoiler</span></s> <u>underline italic bold</u></i> bold</b>
<a href="http://www.example.com/">inline URL</a>
<a href="tg://user?id=123456789">inline mention of a user</a>
<tg-emoji emoji-id="5368324170671202286">👍</tg-emoji>
<code>inline fixed-width code</code>
<pre>pre-formatted fixed-width code block</pre>
<pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>
<blockquote>Block quotation started\nBlock quotation continued\nThe last line of the block quotation</blockquote>
<blockquote expandable>Expandable block quotation started\nExpandable block quotation continued\nExpandable block quotation continued\nHidden by default part of the block quotation started\nExpandable block quotation continued\nThe last line of the block quotation</blockquote>"""
    await message.reply(h, parse_mode=ParseMode.HTML)


# @Client.on_message(
#     filters.private &
#     filters.via_bot(["@vid", "@gif"])
# )
# async def _(_, m):
#     print(m)
#     await m.reply(str(m.media))

# @Client.on_poll(
# )
# async def _(_, p):
#     print(p)

# @Client.on_chat_member_updated()
# async def _(c, u):
#  await c.send_message(-1001220993104, str(u._raw), message_thread_id=1378275)


@Client.on_callback_query()
async def _(client, callback_query):
    print(callback_query)
    await callback_query.answer()
