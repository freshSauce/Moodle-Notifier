![](https://svgshare.com/i/q1W.svg)
___

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![AGPL 3.0 License][license-shield]][license-url]
[![Telegram][telegram-shield]][telegram-url]



<!-- PROJECT LOGO -->
<br />

  <h3 align="center">Moodle-Notifier</h3>

  <p align="center">
    Tired of not getting your homework assignments? Here's your solution!
    <br />
    Made with a 100% love.
    <br />
    <br />
    <a href="https://github.com/freshSauce/Moodle-Notifier"><strong>Give the project a star!</strong></a>
    <br />
    <br />
    <a href="https://github.com/freshSauce/Moodle-Notifier/issues">Report Bug</a>
    ·
    <a href="https://github.com/freshSauce/Moodle-Notifier/issues">Request Feature</a>
  </p>


<!-- ABOUT THE PROJECT -->
## About The Project

This project was made because many Moodle-based platforms don't send the notifications when needed, so I decided to create my own notifier.
<br/>
I decided to use SQLite to store the credentials and create a monitor that every 10 minutes notifies the user if there's a new homework.

### Main modules
* [Flask](https://palletsprojects.com/p/flask/)
* [requests](https://docs.python-requests.org/en/latest/)

## Bot installation

### Setting up environment variables

In order to run the bot you have to set up the following environment variables:

- BOT_TOKEN - The API key provided by the bot father in Telegram
- ADMIN_ID - Your Telegram ID (you can send a message to [userinfobot](http://t.me/userinfobot) to get your ID)
- SCHOOL_DOMAIN - Your school's domain (e.g: www.school-domain.edu.com)

#### Linux
```bash
export API_KEY="YOUR_API_KEY"
```

#### Windows
##### cmd
```bat
set API_KEY="YOUR_API_KEY"
```
##### PowerShell
```bash
$env:API_KEY="YOUR_API_KEY"
```

And repeat with each enviroment variable.

### Setting up the webhook

If we want to use our bot we need to set up a webhook, i.e., where we can receive the updates Telegram provides us. To achieve that we can use [ngrok](https://ngrok.io/) to get an HTTP/HTTPS URL or any host like [render](https://www.render.com).

If we use render to host our Flask app it automatically will set up an URL for us, however, if we use ngrok instead to get an URL, we need to make sure that ngrok is running on the same host thar we are running our Flask app.

Once we have our URL and Flask app running, we need to make a request to [setWebhook](https://core.telegram.org/bots/api#setwebhook) Telegram's endpoint.

### Running the bot

You have 2 ways to run the bot:
- Using the flask module
- Using a WSGI Server (such as Gunicorn)
  
#### Using Flask module

To start the bot using the Flask module you need to set up the "FLASK_APP" environment variable:

##### Linux
```bash
export FLASK_APP="app:app"
```

##### Windows
###### cmd
```bat
set FLASK_APP="app:app"
```
###### PowerShell
```bash
$env:FLASK_APP="app:app"
```
Once you've set your environment variables you can run your bot with:

```bash
python -m flask run
```
or
```bash
flask run
```

#### Using a WSGI Server

There are multiple WSGI containers to choose from, here we will choose [gunicorn](https://gunicorn.org/) as it is the easiest to set up.

First of all you need to install it via PIP

```bash
pip install gunicorn
```

Once we've done that we can start our Bot by doing
```bash
gunicorn app:app
```

And that's it, we should see our Bot being started :)


### Usage of the bot

The bot is pretty much user-friendly, for now, we only have 2 commands (excluding the /help command):

- /login <USERNAME> <PASSWORD> - Used to login into the school's platform. If succeed it will return a message saying that the monitor has started. Otherwise an error will be shown 
- /tareas - Used to force a retreive of all the available homeworks. On error if the user is logged it will log in again, if not, it will prompt the user to log in.
- /deletedb - Used to delete all the data in the database.

And that's it! you now know how to use the bot:).

<!-- CONTRIBUTING -->
## Contributing

Wanna contribute to the project? Great! Please follow the next steps in order to submit any feature or bug-fix :) You can also send me your ideas to my [Telegram](https://t.me/freshSauce), any submit is **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the AGPL-3.0 License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Telegram: - [@freshSauce](https://t.me/freshSauce)

Project Link: [https://github.com/freshSauce/Moodle-Notifier](https://github.com/freshSauce/Moodle-Notifier)

<!-- CHANGELOG -->

### Changelog

#### 0.1.0
* Code uploaded to Github.





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/freshSauce/Moodle-Notifier.svg?style=for-the-badge
[contributors-url]: https://github.com/freshSauce/Moodle-Notifier/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/freshSauce/Moodle-Notifier.svg?style=for-the-badge
[forks-url]: https://github.com/freshSauce/Moodle-Notifier/network/members
[stars-shield]: https://img.shields.io/github/stars/freshSauce/Moodle-Notifier.svg?style=for-the-badge
[stars-url]: https://github.com/freshSauce/Moodle-Notifier/stargazers
[issues-shield]: https://img.shields.io/github/issues/freshSauce/Moodle-Notifier.svg?style=for-the-badge
[issues-url]: https://github.com/freshSauce/Moodle-Notifier/issues
[license-shield]: https://img.shields.io/github/license/freshSauce/Moodle-Notifier.svg?style=for-the-badge
[license-url]: https://github.com/freshSauce/Moodle-Notifier/blob/master/LICENSE
[telegram-shield]: https://img.shields.io/badge/-@freshSauce-black?style=for-the-badge&logo=telegram&colorB=0af
[telegram-url]: https://t.me/freshSauce