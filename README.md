## Introduction

This program will look up Billboard's Top 100 songs from any date and create a 
private Spotify playlist of those songs.


## Manually Accessing the Billboard Top 100 Songs

The Billboard top songs list is at:

https://www.billboard.com/charts/hot-100/

The Billboard site allows you to look up the songs from any date.
You can do so by using the date selector menu at the top of the site, or by typing in a URL with the format:

https://www.billboard.com/charts/hot-100/YYYY-MM-DD

## Setup

### 1. Create a Spotify account
In order to create a playlist in Spotify, you must have an account with Spotify.  If you don't already have an account, you can sign up for a free one here: 

http://spotify.com/signup/

### 2. Create a new Spotify App in the Spotify Dashboard
Once you've signed up and signed in to Spotify, go to the developer dashboard at: 

https://developer.spotify.com/dashboard/

On the Dashboard page, click the "Create An App" button.\
For "App Name", enter any name (e.g. "Billboard to Spotify").\
For "App Description", enter any description (e.g. "Take Billboard's Top 100 songs list from a date in the past to create a Spotify playlist.")\
Click "Create".

### 3. Copy the Spotify App's "Client ID" and "Client Secret"
After creating the new Spotify app, it will appear on your dashboard.  Click it.\
The next screen's top-left corner will show the app's "Client ID" and "Client Secret" (click "Show Client Secret" to reveal it).\
Copy these two strings for the next step.

### 4. Create a ".env" file.
In the same folder as "main.py", create a new file called ".env".
Using any text editor, add the following 2 lines to the .env file:
```
SPOTIFY_CLIENT_ID=YOUR_CLIENT_ID
SPOTIFY_CLIENT_SECRET=YOUR_CLIENT_SECRET
```

Here is an example:
```
SPOTIFY_CLIENT_ID=fdfbcba2f18a49cf87aa440a8eafac57
SPOTIFY_CLIENT_SECRET=3d61a121cb0b4b8f9c19a61013847463
```

### 5. Set the Spotify App's "Redirect URI"
In the Spotify developer dashboard, on your app's page click the green "Edit Settings" button at the top-right.

In the "Redirect URIs" section, type in 
```
http://example.com
```
and click "Add".  Then at the bottom, click "Save".

### 6. Authenticate with Spotify for the first time
Run "main.py".  
If Spotify authentication is successful, you should see a Spotify webpage appear asking you to agree.

Then it will take you to a page with a URL starting with "example.com/..."

Copy the entire URL.  In the Python console where you're running "main.py", you'll see a console prompt "Enter the URL you were redirected to."  Paste in the entire URL and hit Enter.

If successful, a file called "token.txt" will be generated in the same folder as "main.py".

### 7. You are now able to run the program!