# Crib Dragging Auto Cracker
The project is to crack crib dragging in an efficient way. It will crib drag 10,000 most common English vocabularies on the cipher text and collect all the words that are partially/entirely recognized as an English word. The method saves us a lot of time on going through thousands of impossible matches. It also provides us the potential to start the dragging trial from longer length word, which turns out to be most likely to existed. To reveal the real plain text, please use the great crib dragging tools from https://github.com/SpiderLabs/cribdrag to help the cracking while generating a bunch of high possible candidates from this project.

## Usage
Please provide your HEX in the auto.py:
```CIPHER_HEX = "<YOUR_HEX>"```

Run the script
```python auto.py```
