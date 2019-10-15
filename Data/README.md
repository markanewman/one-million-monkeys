# Data

Data is sourced from [here][shakespeare].
The [robots.txt](http://shakespeare.mit.edu/robots.txt) file seems malformed, so I am guessing it intends to prevent all access

```{shell}

```

## Steps

1. Navigate to the [main page][shakespeare].
2. Navigate to the play
3. Use the "Entire play" view
4. Save the play in `./data/raw` using the right mouse button.
   Please save the HTML as "Webpage Only"
5. Run the Parsing script
```{shell}
python parse_plays.py
```


[shakespeare]: http://shakespeare.mit.edu/
