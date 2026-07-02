---
title: "Handling Secrets and API Keys"
---

# Handling Secrets and API Keys

Sooner or later your scripts will need a password, an API token, or a database key. Where you put those secrets matters: a key hard-coded into a script and pushed to [GitHub](version-control-git.md) is a public leak that anyone can find and abuse.

## The Two Golden Rules

1. **Never hard-code secrets** (passwords, tokens, API keys) directly in scripts.
2. **Never commit secrets to Git.** Once pushed, assume the secret is compromised forever, even if you delete it later, it lives in the history.

### Incorrect: Secret in the Source

```r
# DON'T DO THIS -- the key is now in your code and your Git history
api_key <- "sk_live_9f83nZ2xQ1pLmR7t"
response <- httr::GET("https://api.example.com/data",
                      httr::add_headers(Authorization = api_key))
```

### Correct: Read the Secret from the Environment

```r
# DO THIS -- the key lives outside the code
api_key <- Sys.getenv("EXAMPLE_API_KEY")
response <- httr::GET("https://api.example.com/data",
                      httr::add_headers(Authorization = api_key))
```

The code is now safe to share; the secret is supplied at runtime by each user's environment.

## Using Environment Variables and Per-User Config

The standard pattern is to store secrets in a per-user config or `.env` file that stays on your machine and is never committed.

### R: `.Renviron` + `Sys.getenv()`

Create a file named `.Renviron` in your home directory (or project root). R reads it automatically at startup.

```bash
# ~/.Renviron  -- one KEY=value per line, no quotes, no "export"
EXAMPLE_API_KEY=sk_live_9f83nZ2xQ1pLmR7t
DB_PASSWORD=hunter2
```

```r
# In your script -- read, never hard-code
key <- Sys.getenv("EXAMPLE_API_KEY")

# Edit .Renviron conveniently with:
usethis::edit_r_environ()
```

Restart R after editing `.Renviron` for changes to take effect.

### Python: `os.environ` + a `.env` File

Store secrets in a `.env` file and load them with `python-dotenv`.

```bash
# .env  -- keep this file out of Git
EXAMPLE_API_KEY=sk_live_9f83nZ2xQ1pLmR7t
DB_PASSWORD=hunter2
```

```python
import os
from dotenv import load_dotenv

load_dotenv()                       # reads .env into the environment
api_key = os.environ["EXAMPLE_API_KEY"]   # KeyError if missing (fail loud)
db_pw = os.environ.get("DB_PASSWORD")     # returns None if missing
```

### Julia: `ENV[...]`

Julia exposes environment variables through the `ENV` dictionary.

```julia
# Read a variable set in your shell or a .env file
api_key = ENV["EXAMPLE_API_KEY"]

# With a default if it may be unset
db_pw = get(ENV, "DB_PASSWORD", "")
```

You can populate `ENV` from a `.env` file using the `DotEnv.jl` package (`using DotEnv; DotEnv.load!()`).

## Keep Secret Files Out of Git

Add your secret files to `.gitignore` so they can never be accidentally committed.

```bash
# .gitignore
.env
.Renviron
secrets.yaml
*.pem
```

Do check `git status` before committing to confirm no secret files are staged. Don't assume a file is safe just because you "meant" to ignore it, verify the `.gitignore` is working.

## What to Do If You Leak a Key

If a secret ever lands in a commit, a shared log, or a screenshot, **rotate it immediately**:

1. Log in to the provider and **revoke/regenerate** the key. The old value should stop working.
2. Update your local `.env` / `.Renviron` with the new value.
3. Removing it from Git history (with tools like `git filter-repo`) is good hygiene, but rotation is what actually protects you, treat the leaked key as permanently compromised.

## Keyring Options

For extra security, store secrets in your operating system's encrypted credential store instead of a plain-text file:

- **R:** the `keyring` package (`keyring::key_set("EXAMPLE_API_KEY")`, `keyring::key_get(...)`).
- **Python:** the `keyring` library, which talks to macOS Keychain, Windows Credential Locker, or Linux Secret Service.

These avoid having any secret sitting in a readable file at all.

## Related

- [Version Control with Git & GitHub](version-control-git.md)
- [Good Programming Practices](good-programming-practices.md)
- [Reproducibility](reproducibility.md)
- [Project Workflow](project-workflow.md)
- [Programming & Computing](../programming.md)
