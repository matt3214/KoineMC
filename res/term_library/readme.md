# About the `term_library.csv` and `term_library_unique.csv` files

These files are part of the creation of a term library.

This term library is designed to contain term-by-term definitions that are provided as context when a prompt is made to translate a given lang entry.
This will hopefully help to make entries more consistent, as the robot will not translate a given phrase differently if it is given reference to an existing translation of that word alone.

The library was generated with the following prompt to ChatGPT 4

```python
response = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
    {
      "role": "system",
      "content": "Translation:\nI will give you a Minecraft related term to translate into Koine / Classical Greek.\nI will also give you some context by giving you the key that the game uses to refer to the text.\nMake sure to include accent marks and other diacritical marks! Modern Greek is not to occur, so breathing marks are required on vowels that start words. Please use only classical and Koine era Greek with a focus on New Testament terms.\nRemember that the context of all of these is the videogame Minecraft. There are terms related to GUI and also terms relating to in game items."
    },
    {
      "role": "user",
      "content": "Please start by reading this large chunk of the MC lang file and make a list of 10-30 key words in Minecraft, along with a creative guess at translation. Please output a valid CSV with two columns\nExample csv:\n\"phantom\",\"τὸ φάντασμα\"\n\"pillager\",\"ὁ ληστής\"\n\"powder snow\",\"ἡ πούδρα χιόνος\"\n\"leather boots\",\"τὰ δερμάτινα ὑποδήματα\"\n\"rabbit\",\"ὁ λαγός\""
    },
    {
      "role": "user",
      "content": "<about 200 rows from the lang file>"
    }
  ],
  temperature=0.15,
  max_tokens=2073,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
```

Note: I selected chunks of the lang file and placed these chunks in the second "chat entry" after this prompt.

I ran this about 10 times with different representative sections of the lang file (the LLM sometimes outputted way more than 30 rows of CSV)

Next, I run the `term_library_cleanup.py` to prepare the library by removing duplicates and removing underscores from the content in the `term` column (to aid with join operations).