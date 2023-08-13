---
title: "Advanced Python: The lambda"
datePublished: Fri Feb 03 2023 15:58:40 GMT+0000 (Coordinated Universal Time)
cuid: clfmq96ex000309l24mmwadtl
slug: advanced-python-the-lambda
canonical: https://medium.com/@birnadin/advanced-python-the-lambda-3899a4ac5875
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1679673487891/61ac1b6f-6db1-4282-a6ec-42c87ddead58.png
tags: lambda, python, tips, functional-programming, advanced

---

Ever had to write this…

```javascript
def func(n):
  # only allow `l` no of characters in the `n` string
  return n[:l+1]

parsed_n_s = map(seq, func)
```

When you could have done this…

```javascript
# only allow `l` no of characters in the `n` string
parsed_n_s = map(seq, lambda n: n[:l+1]) # is this more readable?
```

Read along to learn WTF is this *lambda* anyway.

## **2 kinds of Python functions**

Python supports two kinds of functions, no, I am not talking about a standalone function and a method of a class. I meant *named* and ***anonymous*** functions. If you have been doing it the first way, you know what named functions are. For the record,

```javascript
def func(param):
  # body
  pass
```

And the anonymous goes like

```javascript
lambda param: pass #body
```

Anonymous means you don’t get to call it by a name. It’s just temporary, a quickie. But you can go out of your way and can do this though.

```javascript
func = lambda param: pass # body
```

This style might help you if the function body is so simple and writing the whole `def ...` shenanigan is a waste of time, space, and effort.

# **Quickie, not Shorty**

Even though *lambda* seems simple, it is so powerful enough to execute somewhat complex logic. Not flexible as the *named* function though 🤷‍♂️. How complex you asked?

This 👇

![](https://miro.medium.com/v2/resize:fit:700/1*Si7DfPZaXGMK4Wu1_8QtDQ.png)

extract from another post

Can become, this 👇

![](https://miro.medium.com/v2/resize:fit:700/1*2CgBK0LxWfdwSqqXkIQFUw.png)

another extract from the same post

I wouldn’t recommend this kind of one-liner in a prolonged codebase, but for quick scripts it does the job pretty well, saving some typing time. For context, please read my post on [Python Comprehension](https://medium.com/@birnadin/advanced-python-comprehensions-c6914520323a).

## [Advanced Python: Comprehensions](https://medium.com/@birnadin/advanced-python-comprehensions-c6914520323a)

### [Powerful one-liners for generators in python3](https://medium.com/@birnadin/advanced-python-comprehensions-c6914520323a)

[medium.com](http://medium.com)

> ***lambda*** *functions always return something; hence* ***lambda*** *never gets* `void` as its return type, and the last execution will implicitly return the result.

# **Applications**

Before applying the *lambda* let’s just summarize: -

* defines an anonymous function,
    
* implicitly *(no need for return lexeme)* returns the result of the last logic,
    
* cannot span to multiple lines (if I am wrong, let me know in the comments or [dm](https://twitter.com/birnadin) me).
    

I guess that’s it. Without ado let’s get started

## **1\. along with map**

I extensively use lambda in the `map` if the logic is simple or can be included in one line. Say, you have a list of strings of varying length, but you need to cut everything down to 120 words (maybe you are doing a Twitter clone with tkinder and python, I don't know 🤷‍♂️)

```javascript
tweets = [...] # the initial tweets
tweets = map(lambda t: t[:121], tweets)
```

If it weren’t for *lambda*s, then that one-liner would be…

```javascript
tweets = [...] # the initial tweets
parsed_tweets = []
for t in tweets:
  parsed_tweets.append(t[:121])
# now parsed_tweets is, parsed 😁
```

Which one do you prefer, I prefer the first one as it is more precise and requires less mental effort to comprehend.

## **2\. along with filter**

Just like `map`, *lambda* is so useful when using `filter`. E.g., If you are to generate odd number series from 1 to `n`, **in front of your crush**, then with *lambda* you could just,

```javascript
gen_odd = lambda n: [i for i in filter(lambda i: i%2, range(1,n+1)]
```

without *lambda,* you would be mopping the floor like…

```javascript
def gen_odd(n):
  result = []
  for i in range(1,n+1):
    if i % 2 != 0:
      result.append(i)
  return result
```

> *It is assumed that your crush is either a noob in python or a JavaScript developer.*

Of course, You could have done this,

```javascript
result = [i for i in range(1, n+1, 2)]
```

But where’s fun in that 😜, when she’s watching. Be careful not to mess up anything or you will be this meme.

![the infamous meme of Joe Biden falling before AirForce 1](https://miro.medium.com/v2/resize:fit:500/1*ADysSuGoXa1wJB6uJGBTlA.jpeg)

from [imgflip.com](http://imgflip.com)

## **3\. saving some characters to type**

Instead of spanning 2 lines of code to square a number or raise a number to power of something else, you can do it in one line with few whitespaces (assuming you can’t use `pow` std utility)

```javascript
def pow_1(x,n):
  return x ** n

pow_2 = lambda x,n: x ** n
```

You can see that `pow_2` is tidy and just to the point without any clutter or boilerplate code.

## **4\. in re.sub()**

If you need to substitute some group of characters adhering to pattern iterating over more than 1 specimen, then *regex has* you covered. I especially used this to create [my Template Engine](https://medium.com/@birnadin/how-to-build-a-simple-template-engine-with-python-and-regex-ecb81d711ceb).

## [How to build a simple template engine with Python and regex](https://medium.com/@birnadin/how-to-build-a-simple-template-engine-with-python-and-regex-ecb81d711ceb)

E.g.,

```javascript
import re
specimen = "hello world"
pattern = r'\w+'
final_str = re.sub(pattern, 'WORLD', specimen)
```

Wait, I just want to replace the last part, not just `world` to `WORLD` but any last word should be Upper! Well, *regex*’s *group* and *lambda* are to the rescue…

```javascript
import re
pattern = r'(\w+)\s(\w+)'
final_str = re.sub(pattern, lambda m: m.group(1) + ' ,' + m.group(2).upper(), specimen)
```

Of course, many ways to do this, some of which might be better, but I couldn’t think of any as of writing this. If you think there are other ways with or without lambda but with lesser time complexity, please point them out in the comments, If not give this post a **clap**, wouldn’t cost you any 😍 and follow [me](https://medium.com/@birnadin) 😘.

# **Epilogue**

Alright, that’s all I got for now, if I ever come across anything new about *lambda* I will put it in the comments or just update the post itself, so make sure you **bookmark** it or something. If you ever come across something awesome as well, please comment. Wouldn’t hurt or cost you to share the knowledge 🎊

If you are intrigued and interested, go ahead and **follow** me on [**Medium**](https://medium.com/@birnadin) or on [**Twitter**](https://twitter.com/birnadin)**.**

Till I see you next time, it’s ***me the BE,*** *signing off 👋.*
