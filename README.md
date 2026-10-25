<div align="center">

<img src="https://files.catbox.moe/4dc4qx.svg" width="720" height="auto" alt="OpusMusic Banner"/>

<h2>OpusMusic</h2>

[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)](https://render.com/deploy?repo=https://github.com/kurukshethrathepride/OpusMusic-)

<b>Telegram Group Calls Streaming Bot</b><br>
Supports YouTube, Spotify, Resso, Apple Music, SoundCloud and M3U8 links.

<br>

<a href="https://github.com/TeamAlfaBots/OpusMusic/stargazers">
    <img src="https://img.shields.io/github/stars/TeamAlfaBots/OpusMusic?color=blueviolet&logo=github&logoColor=black&style=for-the-badge" alt="Stars"/>
</a>
<a href="https://github.com/TeamAlfaBots/OpusMusic/network/members">
    <img src="https://img.shields.io/github/forks/TeamAlfaBots/OpusMusic?color=blueviolet&logo=github&logoColor=black&style=for-the-badge" alt="Forks"/>
</a>
<a href="https://github.com/TeamAlfaBots/OpusMusic/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blueviolet?style=for-the-badge" alt="License"/>
</a>
<a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Written%20in-Python-blueviolet?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
</a>

<br><br>

OpusMusic lets you stream high-quality and low-latency audio and video playback into Telegram group video chats.<br>
Built with <b>Python</b>, <b>Pyrogram</b>, and <b>Py-TgCalls</b> — optimized for reliability and easy deployment.

</div>

<hr>

## 🔥𝐅𝖾𝖺𝗍𝗎𝗋𝖾𝗌 ➠

- 🎧 Stream low-latency **audio & video** in real time to Telegram group video chats
- 🌐 Supports **YouTube, Spotify, Apple Music, SoundCloud, Resso & M3U8**
- ⚡ Advanced queue management with auto-play
- 🎛️ Powerful admin controls for group management
- ⚙️ Easy deployment — works on **Local, VPS, or Heroku**
- ❤️ Built with Python + Pyrogram + Py-TgCalls

<hr>

## ☁️ 𝐃𝖾𝗉𝗅𝗈𝗒𝗆𝖾𝗇𝗍 ➠

### ✔️ 𝐏𝗋𝖾𝗋𝖾𝗊𝗎𝗂𝗌𝗂𝗍𝖾𝗌 ➠

- [Python 3.10+](https://www.python.org) installed
- [ffmpeg](https://ffmpeg.org/) installed on your system
- Required variables from [`sample.env`](https://github.com/TeamAlfaBots/OpusMusic/blob/master/sample.env)

| 𝐕𝖺𝗋𝗂𝖺𝖻𝗅𝖾   | 𝐑𝖾𝗊𝗎𝗂𝗋𝖾𝖽 | 𝐃𝖾𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 |
|----------|----------|-------------|
| `API_ID` | ✅ | Telegram API ID from [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | ✅ | Telegram API Hash |
| `BOT_TOKEN` | ✅ | Bot token from [@BotFather](https://t.me/BotFather) |
| `OWNER_ID` | ✅ | Your Telegram user ID |
| `LOGGER_ID` | ✅ | Log channel/group ID |
| `MONGO_URL` | ✅ | MongoDB connection string |
| `SESSION` | ✅ | Pyrogram session string |

> 💡 Generate your session string using [@StringFatherBot](https://t.me/StringFatherBot)

<hr>

<details>
<summary><h3>🐧 Local / VPS Setup (Linux & macOS)</h3></summary>

```bash
git clone https://github.com/TeamAlfaBots/OpusMusic
cd OpusMusic

# Install uv
curl -Ls https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Install dependencies
uv sync --frozen

# Rename and configure environment variables
mv sample.env .env
# Edit .env with your credentials

# Start the bot
bash start
```

</details>

<details>
<summary><h3>🪟 Windows Setup (PowerShell)</h3></summary>

```powershell
git clone https://github.com/TeamAlfaBots/OpusMusic
cd OpusMusic

# Install uv
irm https://astral.sh/uv/install.ps1 | iex

# Install dependencies
uv sync --frozen

# Rename and configure environment variables
mv sample.env .env
# Edit .env with your credentials

# Start the bot
uv run python -m opus
```

> ⭐ You can also use **Git Bash** or **WSL** to run `bash start`

</details>

<details>
<summary><h3>☁️ Deploy to Heroku</h3></summary>

> Click the button below to deploy on Heroku

<a href="https://dashboard.heroku.com/new?template=https://github.com/TeamAlfaBots/OpusMusic">
    <img src="https://img.shields.io/badge/Deploy%20On%20Heroku-blueviolet?style=for-the-badge&logo=heroku&logoColor=white" alt="Deploy on Heroku"/>
</a>

</details>

<hr>

## ⚙️ 𝐂𝗈𝗇𝖿𝗂𝗀𝗎𝗋𝖺𝗍𝗂𝗈𝗇 ➠

Edit `.env` or set variables in your hosting environment:

<details>
<summary>Example <code>.env</code> file</summary>

```env
API_ID=123456
API_HASH=abcdef1234567890
BOT_TOKEN=123456:ABC-DEF
OWNER_ID=123456789
LOGGER_ID=-1001234567890
MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net
SESSION=BQgfh...AA
```

> 📝 Check [`config.py`](https://github.com/TeamAlfaBots/OpusMusic/blob/master/config.py) for all available options.

</details>

<hr>

## 🧐 𝐔𝗌𝖺𝗀𝖾 ➠

1. Add the bot to your Telegram group
2. Promote it as **admin** with invite users permission
3. Use commands in the chat to control playback:

<details>
<summary>Commands overview</summary>

| 𝐂𝗈𝗆𝗆𝖺𝗇𝖽 | 𝐃𝖾𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 |
|---------|-------------|
| `/play [song/link]` | Play audio in the video chat |
| `/vplay [song/link]` | Play video in the video chat |
| `/pause` | Pause playback |
| `/resume` | Resume playback |
| `/skip` | Skip to next track |
| `/stop` | Stop playback |
| `/seek` | Seek through the stream |
| `/queue` | Show current queue |

</details>

<hr>

## 🛠️ 𝐓𝗋𝗈𝗎𝖻𝗅𝖾𝗌𝗁𝗈𝗈𝗍𝗂𝗇𝗀 ➠

<details>
<summary>Common Issues</summary>

**Bot not joining voice chat?**
- Make sure bot is promoted as admin
- Check if `SESSION` string is valid and has voice chat permissions

**`ffmpeg` not found error?**
```bash
# Ubuntu/Debian
sudo apt install ffmpeg -y

# macOS
brew install ffmpeg
```

**Session string invalid?**
- Re-generate using [@StringFatherBot](https://t.me/StringFatherBot)
- Make sure the account is not banned or restricted

</details>

<hr>

## ❤️ 𝐂𝗈𝗇𝗍𝗋𝗂𝖻𝗎𝗍𝗂𝗇𝗀 ➠

Contributions are welcome!

1. Fork the repository
2. Create your branch: `git checkout -b feature/new`
3. Commit changes: `git commit -m 'New feature'`
4. Push: `git push origin feature/new`
5. Open a Pull Request

<hr>

## 🗒️ 𝐋𝗂𝖼𝖾𝗇𝗌𝖾 ➠

This project is licensed under the **MIT License** — see [LICENSE](https://github.com/TeamAlfaBots/OpusMusic/blob/master/LICENSE) for details.

<hr>

## 🤞 𝐔𝗉𝖽𝖺𝗍𝖾𝗌 & 𝐒𝗎𝗉𝗉𝗈𝗋𝗍 ➠

- 📢 [Updates Channel](https://t.me/TeamAlfaBots)
- 💬 [Support Group](https://t.me/TeamAlfaBotsSupport)

<hr>

## 👀 𝐀𝖼𝗄𝗇𝗈𝗐𝗅𝖾𝖽𝗀𝖾𝗆𝖾𝗇𝗍𝗌

- Inspired by other open-source Telegram music bots
- Thanks to all the [contributors](https://github.com/TeamAlfaBots/OpusMusic/graphs/contributors)

<hr>

<div align="center">

⭐ Enjoying the tunes? **Star the repo** — it keeps the rhythm going!

</div>
