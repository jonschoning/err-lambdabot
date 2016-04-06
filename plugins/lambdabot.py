from errbot import BotPlugin, botcmd, re_botcmd, logging
from errbot.backends.base import ONLINE

import subprocess, re, os

class lambdabot(BotPlugin):

    def activate(self):
        super(lambdabot, self).activate()

    @re_botcmd(pattern=r"^(`|```)\s*> ", prefixed=False, flags=re.IGNORECASE)
    def lambdabot_eval_cmd(self, msg, match):
        return self.lambdabot_go(msg, msg.body)

    @re_botcmd(pattern=r"^(`|```)\s*@(?!(list|help)\s*(`|```)?\s*$)", prefixed=False, flags=re.IGNORECASE)
    def lambdabot_reg_cmd(self, msg, match):
        return self.lambdabot_go(msg, msg.body)

    @re_botcmd(pattern=r"^(`|```)\s*:(t|k|type|kind) ", prefixed=False, flags=re.IGNORECASE)
    def lambdabot_reg_cmd_short(self, msg, match):
        return self.lambdabot_go(msg, msg.body)

    @re_botcmd(pattern=r"^(`|```)\s*(!|:|@)(list|help)\s*(`|```)?\s*$", prefixed=False, flags=re.IGNORECASE)
    def lambdabot_list(self, msg, match):
        return "\`\`\`:t | @type | :k | @kind | > (expr) | @hoogle | @pl | @unpl | @unmtl | @undo | @do | @let | @define | @undefine | @djinn | @pretty | @src\`\`\`"

    def lambdabot_go(self, msg, txt):
        txt_shell = txt
        txt_shell = re.sub(r"^\s*(```|`)\s*","", txt_shell)
        txt_shell = txt_shell.replace(r"```","")
        txt_shell = re.sub(r"`\s*$","", txt_shell)
        txt_shell = re.sub(":(k|kind)","@kind", txt_shell)
        txt_shell = re.sub(":(t|type)","@type", txt_shell)
        txt_shell = txt_shell.replace('“','"')
        txt_shell = txt_shell.replace('”','"')
        logging.info(txt_shell)

        trusted = ['base','bytestring','containers','array','microlens','random','lambdabot-trusted','time', 'stm']
        
        env = os.environ
        env["LC_CTYPE"] = "C"
        p_lambdabot = subprocess.Popen(['lambdabot']+['-t'+ x for x in trusted]+['-lWARNING', '-e'+txt_shell], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)

        stdout, stderr = p_lambdabot.communicate()
        p_lambdabot.stdout.close()
        
        out = stdout.decode(encoding="utf-8", errors="ignore")
        # logging.info(out)

        outSlack = "\`\`\`"+out.replace("*","\*").replace("`","\`")+"\`\`\`"
        logging.info(outSlack)

        if (len(out)>0):
            return outSlack
        else:
            return "<error>"


    # def callback_presence(self, presence):
    #     logging.info(presence)

    def callback_room_joined(self, room):
        logging.info(room)

    # def callback_message(self, msg):
    #     pass

    # def callback_user_joined_chat(self, conn, presence):
    #     pass

