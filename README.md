
# Birdini BirdBuddy Discord Companion

Birdini is a Discord bot that utilises post notifications, images, and videos from your BirdBuddy into a Discord channel, right as the magic happens. Share all those wonderful bird sitings with your community and friends automatically!


![alttext](https://imgur.com/AbA50Py.png)





## Commands

| Command | Arguments     | Description                |
| :-------- | :------- | :------------------------- |
| `/channel` | `channel` or `channelID` | Set which channel you want Birdini to post noitifications to. |
|`/muted_channel`| `channel` or `channelID` | Set which channel you want Birdini to post notifications to when muted (private channel recommended).|
|`/mute` | `None`| Birdini will no longer post messages in the primary channel and send them to the defined muted channel instead.
|`/unmute`|`None`| Birdini will continue to post messages in the primary channel defined.


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file or use the template provided in the Git.

`DISCORD_TOKEN`
Discord bot token that can be gotten from https://discord.com/developers.

`BB_NAME`
This is the email used to log into your BirdBuddy account. Note that this has to be an email/password login and can not be an integration like login with Google. A good work around for this issue (if your primary account is using such type of login). Is to create a new account using an email and then inviting them to be a guest at your feeder.

`BB_PASS`
This is the password used to log into your BirdBuddy account.

# Setup Guide
This makes use of the [pybirdbuddy](https://github.com/jhansche/pybirdbuddy/releases/tag/v0.0.14) library for API calls.

### Files
How to aquire and arrange all the files needed in order to get Birdini to work.
- [Download](https://github.com/jhansche/pybirdbuddy/releases/tag/v0.0.14) the pybirdbuddy library. Birdini was built using v0.0.14. Newer versions may work but v0.0.14 is recommended.
- Create a new folder, I will be calling mine Birdini Bot for the sake of this guide.
- Place the pybirdbuddy-0.0.14 folder inside your new one and rename it `pybirdbuddy`.
- Download the files from this Git and place them in your Birdini Bot folder.
- You should then end up with a folder looking like this: ![alttext](https://i.imgur.com/jbLGL7q.png)
- Insert the appropriate information into your .env file. Do not worry yet about the `DISCORD_TOKEN` as we will be getting this next.


### Discord Bot

A brief guide on how to create a Discord bot and obtain your `DISCORD_TOKEN`.
- Go to https://discord.com/developers/applications
- Click "New Application" in the top right and name your bot.
- Go to the "Bot" section, disable "PUBLIC BOT" and enable all other settings.
- Press "Reset Token" towards the top of the page and copy your new token.
- Add the copied token to your .env file. It should look like this `DISCORD_TOKEN=1234567890`
- Go to the "OAuth2" section and select "URL Generator".
- Select the "bot" tickbox and then the "Administrator" tickbox that will appear in the new interface below.
- Copy the link generated at the bottom, paste it into your browser, and add the bot to your server.

### Setting up AWS (free)
How to setup and host your bot 24/7, for free using AWS!
- Go to https://aws.amazon.com/
- Press the "Sign in to the console" button in the top right.
- You will be redirected to a login screen. Log in or create your account.
- On the "Console Home" page you can scroll down and see a "Build a solution" header.
- Under this header you will see "Launch a virtual machine (With EC2)", select this.
- Ensure that the Application and OS Images are set to "Amazon Linux" (it should be this by default but check anyway).
- Scroll down further until you see "Key pair (login)". Select "Create a new key pair".
- Name this whatever you like and leave it on the default settings.
- When this is all done press the "Launch instance" button on the right side.
- At the very top left of the screen you can click the word "Instances" to be taken to your list of instances.
- It may take some time to setup, just wait until Instance state says "Running" and the status checks have passed.

Now the instance is created we are going to need to upload our files and install some Python dependencies. We will need some additional software to easily upload our files to the AWS. I will be using FileZilla  for this guide which can be found [here](https://filezilla-project.org/).

- We are going to need to connect to our server using FileZilla. To see the information we are going to need we should click the string of bluee text under Instance ID.
- Now open FileZilla and select Edit > Settings
- Locate the "SFTP" section and select "Add key file". This is what we download earlier when we created a new key pair.
- Once this has been selected we can exit out of the settings menu and navigate to File > Site Manager.
- Press "New site". Change the Protocol to SFTP.
- For the Host we are going to want to enter public IPv4 address that can be seen on our instance page. E.g 3.95.161.48
- Under User enter `ec2-user` and press connect.
- On the left hand side we are going to locate our Birdini Bot folder.
- You should now see something like this. ![alttext](https://i.imgur.com/M2CZuJI.png)
- Highlight and drag over all the files into the ec2-user folder.
- Now we have all our files on the server we just need to install some dependencies via the console and we can get the bot running!
- Head back to your AWS instance web page and selec the "Connect" button in the top right, press connect again. This will take you to the AWS console.
- Type `sudo yum install python3-pip`. You will then be asked if this is ok, type `y` and press Enter.
- We can now install the other dependencies using the following commands.
- pip install discord
- pip install python-dotenv
- pip install langcodes
- pip install python_graphql_client
- Now that all our dependencies are finally installed we are ready to start the bot! We will be using the screen command to do this.
- Type `screen -d -m python3 bot.py`.
- The bot should now be running, appear online in discord, and be ready to send notifications!
- If you want to shutdown the bot for whatever reason you can type `screen -ls` to see a list of detatched instances you have running (this should just be one).
- Now to shut this down you want type `screen -X -S [session you want to kill] quit`.
- The session name shown using `screen -ls` will always be different so bare that in mind.
- Here's what my command looked like `screen -X -S 3945..ip-172-31-93-222 quit`
- `3945..ip-172-31-93-222` was the session name that AWS generated for me.



