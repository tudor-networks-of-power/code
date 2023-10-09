less wordlist | xargs -I{} python multitrend.py {}
less wordlist | xargs -I{} convert -density 300 -rotate 90 {}.ps {}.jpg
less wordlist | xargs -I{} grep -n {} extractchanges.out 