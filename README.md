<div align="center">

# ✨ AminoLightPy ✨

<img src="https://github.com/AugustLigh/AminoLightPy/assets/125802350/ba1ae102-dee9-45ab-95c4-f5c5e0249d26" alt="AminoLightPy Banner" width="85%">

### 🚀 Elegant and powerful Python framework for creating AminoApps bots and scripts

[![GitHub release](https://img.shields.io/github/release/AugustLigh/AminoLightPy.svg?style=for-the-badge&color=informational&logo=github)](https://github.com/AugustLigh/AminoLightPy/releases)
[![Documentation](https://img.shields.io/website?down_message=failing&label=docs&up_color=success&up_message=available&url=https://aminopy.readthedocs.io/en/latest/index.html&style=for-the-badge&logo=gitbook)](https://aminopy.readthedocs.io/en/latest/index.html)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge&logo=opensourceinitiative)](https://github.com/AugustLigh/AminoLightPy/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)](https://python.org)

---

### 📍 Quick Navigation
**[🔥 Features](#-features)** • **[⚡ Quick Start](#-quick-start)** • **[📖 Documentation](#-documentation)** • **[🎯 Examples](#-examples)** • **[💬 Support](#-support)**

</div>

---

## 🌟 Features

<div align="center">

<table>
<tr>
<td align="center" width="33%">

### ⚡ **Performance**
Optimized code with maximum efficiency and minimal resource usage

</td>
<td align="center" width="33%">

### 🔄 **Compatibility** 
Seamless backward compatibility with existing Amino bot projects

</td>
<td align="center" width="33%">

### 🎮 **Rich Commands**
Advanced command system with extensive API coverage

</td>
</tr>
<tr>
<td align="center">

### 📱 **iOS Support**
Works on iPhones without jailbreak or restrictions

</td>
<td align="center">

### 🛡️ **Reliable**
Built-in error handling and connection management

</td>
<td align="center">

### 🎨 **Flexible**
Easy customization for any bot requirements

</td>
</tr>
</table>

</div>

---

## ⚡ Quick Start

### 💿 Installation

```bash
pip install amino.light.py
```

### 🎯 Your First Bot

```python
from AminoLightPy import Client, SubClient, ChatEvent

# Initialize and login
client = Client()
client.login("your_email@gmail.com", "your_password")

@client.event(ChatEvent.TEXT_MESSAGE)
def on_message(data):
    if data.message.content.startswith('/hello'):
        sub_client = SubClient(comId=data.comId, profile=client.profile)
        sub_client.send_message(
            chatId=data.message.chatId, 
            message="👋 Hello! I'm your new Amino bot!"
        )
```

<div align="center">
<i>🎉 That's it! Your bot is now running and ready to respond to messages.</i>
</div>

---

## 📖 Documentation

<div align="center">

### 🏗️ **Core Components**

</div>

<details open>
<summary><b>🔌 Client - Main Connection Handler</b></summary>

<br>

The `Client` class manages your connection to Amino services and handles global operations.

#### 🚀 **Initialization**

```python
from AminoLightPy import Client

# Basic setup
client = Client()

# Advanced configuration
client = Client(
    deviceId="your_device_id",
    socket_enabled=True,  # Enable real-time events
    proxies={"http": "http://proxy.example.com"}
)
```

#### 🔐 **Authentication Options**

```python
# Universal login (recommended)
client.login("email@example.com", "password123")

# Specific methods
client.login_email("email@example.com", "password123")
client.login_phone("+1234567890", "password123")
client.login_sid("your_session_id")  # Use cached session
```

#### ⚡ **Event System**

```python
@client.event(ChatEvent.TEXT_MESSAGE)
def handle_text(data):
    print(f"📝 Message: {data.message.content}")

@client.event(ChatEvent.IMAGE_MESSAGE)
def handle_image(data):
    print(f"🖼️ Image from: {data.message.author.nickname}")

@client.event(ChatEvent.VOICE_MESSAGE)
def handle_voice(data):
    print(f"🎵 Voice message received!")
```

<div align="center">

**🎯 Available Events**

| Event | Trigger |
|-------|---------|
| `on_text_message` | Text messages |
| `on_image_message` | Image uploads |
| `on_voice_message` | Voice messages |
| `on_youtube_message` | YouTube links |
| `on_sticker_message` | Stickers |
| `on_join_chat` | User joins chat |
| `on_leave_chat` | User leaves chat |

</div>

</details>

<details open>
<summary><b>🏠 SubClient - Community Operations</b></summary>

<br>

The `SubClient` handles all community-specific actions and messaging.

#### 🎯 **Setup**

```python
sub_client = SubClient(comId=123456, profile=client.profile)
```

#### 💬 **Messaging**

```python
# Send text message
sub_client.send_message(chatId="chat_id", message="Hello World! 🌍")

# Send image with caption
with open("image.jpg", "rb") as img:
    sub_client.send_message(
        chatId="chat_id", 
        message="Check this out! 📸",
        file=img
    )

# Mention users
sub_client.send_message(
    chatId="chat_id",
    message="Hey @user, look at this! 👋",
    mentionUserIds=["user_id_here"]
)
```

#### 💾 **Rich Content**

```python
# Embed links with preview
from base64 import b64encode

with open("preview.jpg", "rb") as preview:
    sub_client.send_message(
        chatId="chat_id",
        message="Amazing content! ✨",
        linkSnippet=[{
            "link": "https://example.com",
            "mediaType": 100,
            "mediaUploadValue": b64encode(preview.read()).decode(),
            "mediaUploadValueContentType": "image/jpeg"
        }]
    )
```

#### 🎨 **Content Creation**

```python
# Create blog post
sub_client.post_blog(
    title="🌟 My Amazing Blog Post",
    content="This is where I share my thoughts...",
    imageList=[open("img1.png", "rb"), open("img2.png", "rb")]
)

# Create wiki entry
sub_client.post_wiki(
    title="📚 Helpful Wiki",
    content="Everything you need to know about...",
    icon=open("wiki_icon.png", "rb")
)
```

#### 🎭 **Interactive Features**

```python
# Show typing indicator
with sub_client.typing(chatId="chat_id"):
    # Simulate thinking time
    time.sleep(2)
    sub_client.send_message(chatId="chat_id", message="Done thinking! 💭")

# Show recording indicator
with sub_client.recording(chatId="chat_id"):
    time.sleep(3)  # Prepare voice message
    with open("voice.mp3", "rb") as voice:
        sub_client.send_message(
            chatId="chat_id", 
            file=voice, 
            fileType="audio"
        )
```

</details>

<details open>
<summary><b>👑 Moderation Tools (Staff Only)</b></summary>

<br>

Advanced moderation features for community leaders and staff.

```python
# Content moderation
sub_client.hide(blogId="blog_id", reason="Inappropriate content")
sub_client.feature(time=3, blogId="blog_id")  # Feature for 3 hours
sub_client.unfeature(blogId="blog_id")

# User management
sub_client.ban(userId="user_id", reason="Spam violation")
sub_client.unban(userId="user_id", reason="Appeal approved")
sub_client.strike(
    userId="user_id", 
    time=24, 
    title="Community Guidelines", 
    reason="Inappropriate behavior"
)
sub_client.warn(userId="user_id", reason="Minor rule violation")
```

</details>

---

## 🎯 Examples

<div align="center">

### 🤖 **Bot Examples**

</div>

<details open>
<summary><b>🎮 Command Bot</b></summary>

```python
from AminoLightPy import Client, SubClient
import random

client = Client()
client.login("email", "password")

commands = {
    '/help': '📋 Available commands:\n/dice - Roll a dice\n/joke - Get a random joke',
    '/dice': lambda: f'🎲 You rolled: {random.randint(1, 6)}!',
    '/joke': lambda: random.choice([
        "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem! 💡"
    ])
}

@client.event(ChatEvent.TEXT_MESSAGE)
def handle_command(data):
    message = data.message.content.lower()
    
    if message in commands:
        sub_client = SubClient(comId=data.comId, profile=client.profile)
        
        response = commands[message]
        if callable(response):
            response = response()
            
        sub_client.send_message(
            chatId=data.message.chatId,
            message=response
        )
```

</details>

<details open>
<summary><b>🎨 Welcome Bot</b></summary>

```python
@client.event(ChatEvent.USER_JOINED)
def welcome_user(data):
    sub_client = SubClient(comId=data.comId, profile=client.profile)
    
    welcome_message = f"""
    🎉 Welcome to our community, {data.message.author.nickname}!
    
    📝 Please read our guidelines
    💬 Feel free to introduce yourself
    🤝 Have fun and be respectful!
    """
    
    sub_client.send_message(
        chatId=data.message.chatId,
        message=welcome_message
    )
```

</details>

<details open>
<summary><b>🔄 Auto-Responder</b></summary>

```python
auto_responses = {
    'hello': '👋 Hello there! How can I help you today?',
    'bye': '👋 Goodbye! Have a great day!',
    'thanks': '😊 You\'re welcome! Happy to help!',
}

@client.event(ChatEvent.TEXT_MESSAGE)
def auto_respond(data):
    message = data.message.content.lower()
    
    for keyword, response in auto_responses.items():
        if keyword in message:
            sub_client = SubClient(comId=data.comId, profile=client.profile)
            sub_client.send_message(
                chatId=data.message.chatId,
                message=response
            )
            break
```

</details>

---

## 💬 Support

<div align="center">

### 🤝 **Get Help & Connect**

<table>
<tr>
<td align="center">

**💬 Telegram**
<br>
[@augustlight](https://t.me/augustlight)

</td>
<td align="center">

**💙 Discord**
<br>
engineer48

</td>
<td align="center">

**📚 Documentation**
<br>
[ReadTheDocs](https://aminopy.readthedocs.io/)

</td>
</tr>
</table>

</div>

---

## 🎖️ Contributing

We welcome contributions! Whether it's:
- 🐛 Bug reports
- ✨ Feature requests  
- 📝 Documentation improvements
- 🔧 Code contributions

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/AugustLigh/AminoLightPy/blob/main/LICENSE) file for details.

---

<div align="center">

### 🌟 **Show Your Support**

If this project helps you, please consider giving it a ⭐ on GitHub!

---

<sub>💡 <i>This framework builds upon the foundation of existing Amino libraries, enhanced for simplicity and effectiveness.</i></sub>

<sub>🐍 <i>Compatible with Python 3.10+ • Works on all platforms</i></sub>

</div>
