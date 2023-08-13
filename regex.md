---
title: "Regular Expressions done right"
datePublished: Fri Mar 24 2023 15:50:19 GMT+0000 (Coordinated Universal Time)
cuid: clfmpy4rd00000al25nwpheay
slug: regular-expressions-done-right
canonical: https://medium.com/@birnadin/regular-expressions-done-right-3a73f0deacf4
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1679672442314/d806b7aa-5f3b-46c5-98b8-06ddb7c444f5.png
tags: tips, regex, regular-expressions

---

> *A regular expression (here on, I will refer to as regex) is not scary as the meme states. It just needs a little patience and knowledge of the* ***state diagram.***

---

# **Regex is just State Diagram!**

> *Only sounds fancy, but in a nutshell, it is just a primal flowchart.*

![](https://miro.medium.com/v2/resize:fit:700/1*BtggalwtgftX6t2IemXJOA.jpeg align="left")

from [community.coda.io](http://community.coda.io)

---

Assume, you are to analyze users and their location. Since now a day everyone is anxious about their privacy they tend to mask their location. Your conclusion might be off and bring millions of $ lost. 😳. One way to do it is to ask phone number for 2FA and then analyze the phone number 😜. Just state it vaguely in the T&C or Privacy Policy.

So, phone numbers then, yeah, they have a system and encode location data. But a bump is that you never enforced a pattern to the end-user. So, when you try to look at the head, you see this,

```javascript
000-02-2344
000 02 2343
001.23.2342
023-02-2344
```

Imagine you have a million users or so. WTF! So, you sanitize at pre-processing state. How?

```javascript
user_pns = [user.phone_number for user in Users()]
pns_sanitized = []

for pn in user_pns:
  if '-' in pn:
    # sanitize how ever you want
    pns_sanitized.append(pn.replace('-', ''))
  elif '.' in pn:
    pass
  else:
    pass
```

But, what if someone inputs a phone number as `002-02.2344`. They must have been in hurry, so they mixed up delimiters. Your script will leave `.` out and you have inconsistent data to model. Heck even what if some lunatic used `*` or had `(...)` to indicate the beginning? Are going to write *if, elifs* for all of that?

Do you realize that the fact each branching will penalize the performance write? If not search **CPU Shadow Realm Exploitations**. What should you do? Call parser’s 911, **The Regex.**

No matter how end-user input, the number will always be `xxx xx xxxx` or some other way depending on your users’ locality which you can query from where 2FA codes be sent (Cuz LTE or any cellular protocols require specific country data). Let’s consider the scenario of the pattern I mentioned above.

The pattern `xxx xx xxxx` can be represented as `\D*\d{3}\D*\d{2}\D*\d{4}`. Gibberish? Let me tell you the lexemes or the grammar of **Regex**.

![](https://miro.medium.com/v2/resize:fit:511/1*AAiXM0KwFTFpC-Djt2QskQ.png align="left")

for more, check the link below 👇

## [Regex Cheat Sheet: A Quick Guide to Regular Expressions in Python](https://www.dataquest.io/blog/regex-cheatsheet/)

---

So `\D*\d{3}\D*\d{2}\D*\d{4}` becomes: -

* Interest start can *\** *,* start with non-numeric, `\D`
    
* then 3, `{3}`, numeric`\d`, follow
    
* then optional `*` non-numeric, `\D`
    
* then after 2, `{2}` numeric, `\d`
    
* followed by optional `*` non-numeric
    
* then 4 numeric.
    

OR, you can think of the regex as a map of how a finger should move across a piece of string, a state diagram.

![](https://miro.medium.com/v2/resize:fit:700/1*lnNrjFCFN02DUbl8CeWjsQ.png align="left")

see, I told you 😘

> *Now you can like ❤ the button is at the bottom of the screen 😎.*

Each logical piece represents each state.

* Special characters move the finger (`$ ^` or just EOL), **start or stop** signals,
    
* groups are saved to memory, **output to tape,**
    
* characters indicate progresses of the finger like, move finger if and only if under the finger we have alpha-numeric (`\w`), **creating conditionals,**
    
* length/numbers represent how many times the finger should sense a given character, like 4 times `{4}` or should it be 0. **Creating loops and sequences;**
    
* If by any chance the finger can’t transition to the next state, then the machine terminates and starts from the beginning on another *window* of the specimen.
    

<mark>See, it is just a state machine in disguise. Once you get this fundamental right, you are off to 🚀.</mark>

---

# **The Tip to compile it.**

1. Just take an example and put your finger on the leftmost side of the specimen.
    
2. Ask yourself what you should do to advance to the next character. Should you encounter a numeric or alpha or whitespace.
    
3. Do it till you find yourself at the right-most character of your specimen.
    
4. Now just like you factorize an integer, factorize your state transitions. E.g., if we have 12 then we can write it as `3 x 2 x 2`, that one becomes, `3 x 2^2`. So, we have a 3 and 2 appears `2` times.
    

Now, map it as a state diagram by head or if it is complex, take a piece of paper and just sketch it. No need to follow the symbology or conventions. It just should express what your mind says. Heck even, you can use **Flow Chart**. Because any state-machine or *Turing Machine* can be expressed via a Flow-Chart.

Let’s look at an example. Say, we need to extract the names of people from phone book entries along with prefixes. Step 1 is to get an example.

## **Mas. Birnadin Erick**

1. Put your finger in the leftmost character, `M`.
    
2. Ask what we should do to progress to the right. *We should encounter* ***an*** *alphabet.*
    
3. Then again, ***an*** *alphabet and so.*
    
4. ***A*** *period*, `.`;
    
5. Now ***a*** *whitespace* `_`,
    
6. Now **an** *alphabet*, but in *Uppercase*.
    
7. …
    

If in the diagram, then traces would be…

![](https://miro.medium.com/v2/resize:fit:700/1*hDW4o0KIcukcskby0YdXFw.png align="left")

from the start to 2nd state

![](https://miro.medium.com/v2/resize:fit:700/1*80ips02sIfHQ8PNOpg2kxA.png align="left")

from 2nd to 3rd

![](https://miro.medium.com/v2/resize:fit:700/1*TMPeXddwIJB1uQIlVEhdHw.png align="left")

from 3rd to nth

![](https://miro.medium.com/v2/resize:fit:700/1*JpPIFpdLiXz9yFMv2DNULw.png align="left")

nth to finish.

Are we done? no there is another possible variant!

## **Ms. Jane Doe**

The difference would be from *2nd* to *3rd* we have to scan an s.

![](https://miro.medium.com/v2/resize:fit:700/1*TUAGDMJtlqCBagrWHSbo2g.png align="left")

2nd to 3rd state transition changes

Everything else stays the same, hence a common factor, have we. Done? Nope.

## **Mr. John Doe**

This time, *2nd* to *3rd* trigger is `r`.

So, *2nd* to *3rd* have more than one transition.

![](https://miro.medium.com/v2/resize:fit:700/1*dPUySP4eXsKMhuaci2xf5w.png align="left")

different paths machine can deviate.

And, in between an *nth* and (*n+1)th* state may share the same trigger but multiple times. E.g., along `irnadin` in `Birnadin`, `i` and `r` are the same trigger but have multiple points of presence.

![](https://miro.medium.com/v2/resize:fit:700/1*JMQKg9qjokpCxXS1jj_67w.png align="left")

first pass;

👆 can be simplified as 👇

![](https://miro.medium.com/v2/resize:fit:700/1*9jCWFvJYU2n7_x0LbdhbDQ.png align="left")

simplified on 2nd pass.

So, as a **result,** our state diagram becomes like 👇

![](https://miro.medium.com/v2/resize:fit:700/1*zKxfTXP1qVkyqVbWueQ09Q.png align="left")

click to zoom and analyze 🔍

## **Compilation**

![](https://miro.medium.com/v2/resize:fit:700/1*hDW4o0KIcukcskby0YdXFw.png align="left")

gives: M

![](https://miro.medium.com/v2/resize:fit:700/1*dPUySP4eXsKMhuaci2xf5w.png align="left")

this gives: M\[asr\]

Then the `.` gives us `M[asr]\W*` , there could be presence or absence;

The whitespace gives us, `M[asr]\W*\s*`, there could be more than 1 space due to input errors;

Then an Uppercase: `M[asr]\W*\s*[A-Z]`, you could actually say `\w` instead of `A-Z` if you want;

![](https://miro.medium.com/v2/resize:fit:700/1*9jCWFvJYU2n7_x0LbdhbDQ.png align="left")

we end up with: M\[asr\]\\W\*\\s\*\[A-Z\]\\w\*

The same goes, thus we end up with 👇

```javascript
M[asr]\W*\s*[A-Z]\w*\s*[A-Z]?\w* 
# last [A-Z]?\w* means there could be last name or not

# if you know for sure, prefix is delimitted by period
M[asr]\.*\s*[A-Z]\w*\s*[A-Z]?\w*
```

Do you feel how easy it is? <mark>Told you </mark> **<mark>Regular Expression </mark>** <mark>is just </mark> **<mark>State Diagram </mark>** <mark>in disguise 🐑.</mark>

---

# **Epilogue**

I hope I shed somewhat light on regex using how I understand it. If you disagree or have an example that contradicts, please let me know in the comments, would love to be corrected beforehand.

Another post is coming soon using Regex in Python, Rust and JavaScript.

If you are intrigued or interested in this kind of stuff, make sure you follow me on [**Twitter**](https://twitter.com/birnadin)**.**

Till then, *it’s* ***me the BE,*** *signing off 👋*

Cover background by **Steve Johnson.**