from errbot import BotPlugin, botcmd, re_botcmd, logging
import subprocess, re

class lambdabot(BotPlugin):

    def activate(self):
        super(lambdabot, self).activate()


    @re_botcmd(pattern=r"^:t |^:type ", prefixed=False, flags=re.IGNORECASE)
    def lambdabot_type(self, msg, match):
        return self.lambdabot_go(msg, re.sub("^:t","!type", msg.body))

    @re_botcmd(pattern=r"^:k |^:kind ", prefixed=False, flags=re.IGNORECASE)
    def lambdabot_kind(self, msg, match):
        return self.lambdabot_go(msg, re.sub("^:k","!kind", msg.body))

    @re_botcmd(pattern=r"^>", prefixed=False, flags=re.IGNORECASE)
    def lambdabot_eval(self, msg, match):
        return self.lambdabot_go(msg, msg.body)

    @re_botcmd(pattern=r"^!type|^!kind|^!pl|^!unpl|^!unmtl|^!undo|^!do|^!let|^!define|^!undefine|^!djinn|^!pretty|^!src", prefixed=False, flags=re.IGNORECASE)
    def lambdabot_cmd(self, msg, match):
        return self.lambdabot_go(msg, msg.body)


    def lambdabot_go(self, msg, txt):
        logging.info(txt)

        p1 = subprocess.Popen(['lambdabot', '-e', txt.replace("!","@")], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(['runghc', self.bot_config.BOT_EXTRA_PLUGIN_DIR + '/lambdabot-decode.hs'], stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        stdout, stderr = p2.communicate()
        p2.stdout.close()
        
        out = stdout.decode(encoding="utf-8", errors="ignore").replace("@","!").replace("*","★")
        logging.info(out)

        if (len(out)>0):
            return out
        else:
            return "..."


    def callback_presence(self, presence):
        logging.info(presence)

    def callback_room_joined(self, room):
        logging.warning(room)

    # def callback_message(self, msg):
    #     pass

    # def callback_user_joined_chat(self, conn, presence):
    #     pass

