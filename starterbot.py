import os
import time
import requests
from slackclient import SlackClient

os.environ["SLACK_BOT_TOKEN"] = "{PLACEHOLDER}"
os.environ["SLACK_BOT_ID"] = "{PLACEHOLDER}"
# starterbot's ID as an environment variable
# BOT_ID = os.enviroxn.get("SLACK_BOT_ID")
SLACK_BOT_TOKEN = "{{PLACEHOLDER}}"
BOT_ID = "{{PLACEHOLDER}}"

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = 'do'

def getRandomJoke():
    r = requests.get('http://api.icndb.com/jokes/random')
    r = r.json()
    if r['type'] == "success":
        if r['value'] and r['value']['joke']:
            return r['value']['joke']
    return None

# instantiate Slack & Twilio clients
# BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
BOT_TOKEN = SLACK_BOT_TOKEN
slack_client = SlackClient(BOT_TOKEN)

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    if "joke" in command:
        joke = getRandomJoke()
        response = "Huh jou want to hear a joke so be it. I know a lot of jokes just a sec."
        slack_client.api_call("chat.postMessage", channel=channel,
                              text=response, as_user=True)
        time.sleep(2)
        response = joke;
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            # we do not parse bot responses only humans
            if output and 'text' in output and output['user'] and BOT_ID != output['user']:
                # return text after the @ mention, whitespace removed
                return output['text'].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")



