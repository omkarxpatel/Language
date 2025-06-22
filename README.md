# Version 1 - Python Converter

This is version 1 of my custom coding language. To get a basic idea on how I could do this, I started by implementing some logic inside of a basic python program. Basically, this program will read a .rot file, convert that code into python, and compile it. This is a very simple way to do it as all you need to do is compare your custom keywords to a hashmap which would then be able to convert your syntax into python syntax.

There are three steps to this program. First, the tokenizer, or lexer. The lexer is the part of the program that initially reads the .rot file. Once the files contents has been read, the lexer will convert the code into segments, or tokens. For example, if we take the following code:

```cpp
cout("hello")
```
The tokenizer will first split the code up into tokens, which then would be tranformed into python syntax later on in the parser. We can see below the output of the tokenizer. This process uses regex to look for preset combinations in the text file.
```py
------------------------------
0    |  'cout'    |  PRINT
1    |  '('       |  L_PAREN
2    |  '"'       |  QUOTE
3    |  'hello'   |  STRING
4    |  '"'       |  QUOTE
5    |  ')'       |  R_PAREN
------------------------------
```
Once the tokens have been generated, they are passed into the parser. The parser is the segmet of the code which transforms tokens into python code.
```py
------------------------------
1    |  cout      ->    print
2    |  (         ->    (
3    |  "         ->    "
4    |  hello     ->    hello
5    |  "         ->    "
6    |  , end=""  ->    , end=""
7    |  )         ->    )
------------------------------
```
Each token is compared to values stored in a hashmap. If a keyword or something similar is different from .rot syntax to python syntax, the parser will convert. We can see this mainly in the first operation where the parser converts `cout` into `print`. This is similar to everything else in this language.

Finally, the last step is simple (in this scenario). We use the python built in function `exec()` to execute the parsed code written into the output file. We can see that our main runner file, `main.py`, reads the source file, `main.rot`, and then writes the python equivient into the output file, `output.py`.

Here is what the `output.py` file looks like after execution:
```py
print("hello", end="")
```

Example usecase:
```py
funct hi(x | y) {
    if (x > y) {
        coutln(x)
    }

    elseif (x == y) {
        coutln("same")
    }

    else {
        coutln(y)
    }
}

hi(10 | 10)
```
Now, for version 2 of the code, we will be making our own version of the python `exec()` function along with many other things such as error & syntax handling, custom syntax & keywords, and converting the source code directly into assembly.
