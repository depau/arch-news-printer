# Arch Linux news pretty-printer

Simple script to pretty-print Arch Linux news to a terminal, suitable for MOTD.

The links work ;) <sub><sup>([on many terminals](https://gist.github.com/egmontkob/eb114294efbcd5adb1944c9f3cb5feda))</sub></sup>

![Screenshot](https://i.postimg.cc/RFffVCRX/scree.png)

## Requirements

`python-requests` for downloading the RSS feed and `lynx` to render the news HTML.

## Usage

```bash
./archnews.py         # Prints all news in the RSS feed
./archnews.py 3       # Prints first 3 news
./archnews.py 2 3     # Prints 2 long news with the description, then 3 titles
./archnews.py 0 5     # Print last 5 titles
```

Since the RSS is downloaded every time you run it, it is advisable to instead place it in a cronjob, for example:

```cron
 0 */2 * * *  /bin/bash -c '~/arch-news-printer/archnews.py 1 4 > ~/.cache/archnews.tmp && mv ~/.cache/archnews.{tmp,txt}'
```

then in your shell config:

`.bashrc` / `.zshrc`
```bash
cat ~/.cache/archnews.txt 2>/dev/null
```

`config.fish`
```fish
function fish_greeting
  cat ~/.cache/archnews.txt 2>/dev/null
end
```

## License

GNU GPL v3.0
