<h1 align="center">✨ AminoLightPy ✨</h1>

<p align="center">
  <img src="https://github.com/AugustLigh/AminoLightPy/assets/125802350/ba1ae102-dee9-45ab-95c4-f5c5e0249d26" alt="AminoLightPy Banner" width="80%">
</p>

<p align="center">
  <b>Elegant and powerful Python framework for creating AminoApps bots and scripts</b>
</p>

<p align="center">
    <a href="https://github.com/AugustLigh/AminoLightPy/releases"><img src="https://img.shields.io/github/release/AugustLigh/AminoLightPy.svg?style=flat-square&color=informational" alt="GitHub release" /></a>
    <a href="https://aminopy.readthedocs.io/en/latest/index.html"><img src="https://img.shields.io/website?down_message=failing&label=docs&up_color=success&up_message=available&url=https://aminopy.readthedocs.io/en/latest/index.html&style=flat-square" alt="Docs" /></a>
    <a href="https://github.com/AugustLigh/AminoLightPy/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="licence" /></a>
</p>

<div align="center">
  
  [📋 Features](#features) • 
  [🚀 Usage](#installation-and-usage) • 
  [📝 Example](#example) • 
  [📚 Documentation](#documentation) • 
  [📌 Notes](#notes)
  
</div>

---

## 📋 Features

<div align="center">

| 🔥 Feature | 📄 Description |
|:---:|:---|
| ⚡ **Optimization** | Most of the code has been rewritten for maximum performance |
| ⚙️ **Backward compatibility** | Write code with correct syntax without compatibility issues |
| 🎮 **Commands support** | Go even further with new requests and capabilities |
| 🍎 **Supported on iPhones** | Works for free, without jailbreak and restrictions |

</div>

## 🚀 Installation and Usage

### Install the package

```bash
pip install amino.light.py
```

### Basic usage

Import the `Client` and `SubClient` objects into your bot's code:

```python
from AminoLightPy import Client, SubClient

# Your help message
help_message = """
👋 Welcome!
📚 This is help page.
"""

# Create Client object
client = Client()

# Login into account
client.login("example_mail@gmail.com", "example_password")

# And display the help!
@client.event("on_text_message")
def on_message(data):
    # Do not answer to myself
    if data.message.author.userId != client.profile.userId:
        # Create SubClient object
        sub_client = SubClient(comId=data.comId, profile=client.profile)
        
        # Process help command
        if data.message.content.startswith('/help'):
            sub_client.send_message(chatId=data.message.chatId, message=help_message)
```

## 📝 Example

Simply copy the code above and type `/help` in the chat to see your bot in action.

Also, take a look at interactive examples in our documentation!

## 📚 Documentation

<div align="center">
  <p><b>Complete API reference for building amazing Amino bots</b></p>
</div>

### 🔹 Client

<details open>
<summary><b>Main API connection class</b></summary>

#### 🔸 Initialization

```python
from AminoLightPy import Client

# Initialize client with default settings
client = Client()
# OR
client = Client(socket_enabled=False)
#if you not need websocket (faster)

# With custom settings
client = Client(deviceId="your_device_id", proxies={"http": "http://proxy.example.com"})
```

#### 🔸 Authentication

```python
# Universal login (recommended)
client.login(email_or_phone="example@gmail.com", password="your_password")

# Alternative authentication methods
client.login_email(email="example@gmail.com", password="your_password")
client.login_phone(phoneNumber="+1234567890", password="your_password")
client.login_sid(SID="your_sid_here")  # SIDs are cached automatically when using client.login()

# OR

client.login(email_or_phone="example@gmail.com", password="your_password", self_device=False)
# If you want a random DeviceId for each login
```

#### 🔸 Event Handling

```python
@client.event("on_text_message")
def on_message(data):
    print(f"Received message: {data.message.content}")

@client.event("on_image_message")
def on_image(data):
    print(f"Received image from: {data.message.author.nickname}")
```

<table>
<tr><th>Available Events</th><th>Description</th></tr>
<tr><td><code>on_text_message</code></td><td>Triggered when a text message is received</td></tr>
<tr><td><code>on_image_message</code></td><td>Triggered when an image message is received</td></tr>
<tr><td><code>on_youtube_message</code></td><td>Triggered when a YouTube link is shared</td></tr>
<tr><td><code>on_voice_message</code></td><td>Triggered when a voice message is received</td></tr>
<tr><td><code>on_sticker_message</code></td><td>Triggered when a sticker is received</td></tr>
<tr><td><code>on_join_chat</code></td><td>Triggered when someone joins a chat</td></tr>
<tr><td><code>on_leave_chat</code></td><td>Triggered when someone leaves a chat</td></tr>
</table>
and more...

#### 🔸 Community Operations

```python
# Get list of joined communities
communities = client.sub_clients(size=100)

# Search for a community
found_communities = client.search_community("amino_id")

# Join/Leave community
client.join_community(comId=123456)
client.leave_community(comId=123456)

# Send join request
client.request_join_community(comId=123456, message="i want to join😭🙏")
```
</details>

### 🔹 SubClient

<details open>
<summary><b>Community-specific operations</b></summary>

#### 🔸 Initialization

```python
from AminoLightPy import Client, SubClient

client = Client()
client.login("email", "password")

# Create a SubClient for a specific community
sub_client = SubClient(comId=123456, profile=client.profile)
```

#### 🔸 Messaging

```python
# Text message
sub_client.send_message(
    chatId="chat-id-here", 
    message="Hello world!"
)

# Image message
with open("image.jpg", "rb") as image:
    sub_client.send_message(
        chatId="chat-id-here", 
        file=image
    )
# Warn! You need add `fileType="audio"` for voice message

# Mentions
sub_client.send_message(
    chatId="chat-id-here",
    message="Hello @user!",
    mentionUserIds=["user-id-here"]
)

# Rich content (embedded links)
sub_client.send_message(
    chatId="chat-id-here",
    message="Check this out!",
    linkSnippet={
        "link": "https://example.com",
        "title": "Example Website",
        "mediaType": 100,
        "mediaSourceWidth": 500,
        "mediaSourceHeight": 300
    }
)
```

#### 🔸 Chat Management

```python
# Create a new chat
sub_client.start_chat(
    userId="user-id", 
    message="Hi there!"
)

# Create a group chat
sub_client.start_chat(
    userIds=["user-id-1", "user-id-2"],
    title="Our Group",
    message="Welcome everyone!"
)

# Get joined chats
chats = sub_client.get_chat_threads(start=0, size=100)

# Get chat messages
messages = sub_client.get_chat_messages(
    chatId="chat-id-here",
    start=0,
    size=100
)

# Invite to chat
sub_client.invite_to_chat(
    chatId="chat-id-here", 
    userIds=["user-id-1", "user-id-2"]
)

# Leave chat
sub_client.leave_chat(chatId="chat-id-here")
```

#### 🔸 Content Creation

```python
# Create a blog post
sub_client.post_blog(
    title="My Blog Post",
    content="This is content for my blog post",
    imageList=[open("image_1.png", "rb"), open("image_2.png", "rb")]
)

# Create a wiki
sub_client.post_wiki(
    title="Wiki Title",
    content="Wiki content here",
    icon=open("icon.png", "rb")
)

# Upload media
media = sub_client.upload_media(file=open("image.jpg", "rb"))
```

#### 🔸 Social Interactions

```python
# Comment on content
sub_client.comment(blogId="blog-id", message="Great post!")
sub_client.comment(wikiId="wiki-id", message="Useful information!")

# Like content
sub_client.like_blog(blogId="blog-id")
sub_client.like_comment(commentId="comment-id")

# Follow/Unfollow users
sub_client.follow(userId="user-id")
sub_client.unfollow(userId="user-id")

# Block/Unblock users
sub_client.block_user(userId="user-id")
sub_client.unblock_user(userId="user-id")
```

#### 🔸 Moderation (for staff/leaders)

```python
# Hide content
sub_client.hide(blogId="blog-id", reason="Violates community guidelines")

# Ban/Unban users
sub_client.ban(userId="user-id", reason="Spamming")
sub_client.unban(userId="user-id", reason="Appeal accepted")

# Feature content
sub_client.feature(time=1, blogId="blog-id")
sub_client.unfeature(blogId="blog-id")

# Strike users
sub_client.strike(userId="user-id", time=1, title="Spam", reason="Excessive messaging")

# Warn users
sub_client.warn(userId="user-id", reason="Minor rule violation")
```

#### 🔸 Context Managers

```python
# Show "typing..." indicator
with sub_client.typing(chatId="chat-id-here"):
    # This block will show typing indicator while executing
    time.sleep(2)
    sub_client.send_message(chatId="chat-id-here", message="Hello!")

# Show "recording..." indicator
with sub_client.recording(chatId="chat-id-here"):
    # Prepare a voice message
    time.sleep(3)
    sub_client.send_message(chatId="chat-id-here", file=open("demo.mp3", "rb"), fileType="audio")
```
</details>

<div align="center">
  <p><i>For complete API reference, see the <a href="https://aminopy.readthedocs.io/en/latest/index.html">official documentation</a>.</i></p>
</div>

## 📱 Contact and Support

If you can't find what you're looking for or need help with this library:
- Telegram: [augustlight](https://t.me/augustlight)
- Discord: *engineer48*

We will be glad to help!

## 📌 Notes

> *This is not my original project. Amino libraries already existed before me. I just wanted to create a simple and effective way to support bots.*

> *This framework works only with Python.*