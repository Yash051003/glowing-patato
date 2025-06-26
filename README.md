# Instagram Data Extractor

I got tired of manually checking Instagram profiles for research purposes, so I built this Python script using instagrapi to automate the process. It pulls user data, stories, highlights, and more without having to click through everything manually.

## What it does

- Logs into Instagram and fetches user profile info
- Gets the list of people they're following 
- Downloads active stories with timestamps
- Extracts highlight content (this was tricky - had to implement multiple methods)
- Can also grab recent posts if needed

## Setup

You'll need Python 3.7+ and the instagrapi library:

```bash
pip install instagrapi
```

Then update these variables in the script:
```python
USERNAME = "your_username"
PASSWORD = "your_password" 
TARGET = "profile_to_check"
```

**Note:** Don't push your actual credentials to GitHub! Use environment variables or a config file.

Recent Update: Session Management

I added a separate login function that handles 2FA and saves your session, so you don't have to enter verification codes every single time. Just add the 

```bash
python login_sessions.py (code block in the top of the script)
```

Then replace the simple login in your main function with:
python
# Replace this line:
# client.login(USERNAME, PASSWORD)

# With this:
```bash
python if not login_with_session(client, USERNAME, PASSWORD):
    print("Failed to login, exiting...")
    return
```

This was a game changer - no more entering 2FA codes every time I test the script!

## Running it

Just run:
```bash
python instagram_fetcher.py
```

You'll see output like this:
```
🔐 Logging in...
✅ Login successful!

📄 Username: some_user
📝 Full Name: Some User
👥 Followers: 1234
📸 Posts: 567

👤 Following:
➡️ friend1 | Friend One
➡️ friend2 | Friend Two

📁 Highlights:
📁 Highlight: Vacation (3 items)
   🖼️ Media: https://...
```

## The highlight extraction thing

This was honestly the most annoying part to get working. Instagram's API for highlights is inconsistent, so I ended up implementing three different methods:

1. Standard approach with `user_highlights()`
2. Alternative method with amount parameter
3. Multiple fallback techniques using `story_pk_to_story()` and `reel_media()`

Most of the time the first method works, but sometimes you need the fallbacks so i take some help of claude to find the alternate solution.Which is the third method.

## Limitations & gotchas

- **Private accounts**: Obviously can't access much unless you follow them
- **Rate limits**: Instagram will block you if you make too many requests. I added delays but still be careful
- **2FA**: If you have two-factor auth enabled, you might need to handle the OTP prompt
- **API changes**: This uses Instagram's unofficial API, so it could break if they change things

## Legal stuff

Use this responsibly. Only access public data, respect people's privacy, and don't violate Instagram's ToS. I built this for legitimate research purposes - don't be weird with it.

## Issues I ran into

- Login sometimes fails on first try - just run it again
- Private accounts return limited data (obviously)
- Some highlights don't load properly - that's why I added the multiple extraction methods
- Rate limiting kicked in when I was testing - had to add more delays

## Contributing

Feel free to submit PRs if you find bugs or want to add features. The highlight extraction could probably be improved.

## Why I built this

I was doing social media research for a project and got sick of manually browsing through profiles. This automates the boring stuff so I can focus on analyzing the data instead of collecting it.

---

*Built this over a weekend because I'm lazy and like automating repetitive tasks.*
