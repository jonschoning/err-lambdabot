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

    @re_botcmd(pattern=r"^(`|```)\s*:(t|k|i|type|kind|info) ", prefixed=False, flags=re.IGNORECASE)
    def lambdabot_reg_cmd_short(self, msg, match):
        return self.lambdabot_go(msg, msg.body)

    @re_botcmd(pattern=r"^(`|```)\s*(!|:|@)(list|help)\s*(`|```)?\s*$", prefixed=False, flags=re.IGNORECASE)
    def lambdabot_list(self, msg, match):
        return "\`\`\`:t | @type | :k | @kind | :i | @info | > (expr) | @hoogle | @pl | @unpl | @unmtl | @undo | @do | @let | @define | @undefine | @djinn | @pretty | @src\`\`\`"

    def lambdabot_go(self, msg, txt):
        txt_shell = txt
        txt_shell = re.sub(r"^\s*(```|`)\s*","", txt_shell)
        txt_shell = txt_shell.replace(r"```","")
        txt_shell = re.sub(r"`\s*$","", txt_shell)
        txt_shell = re.sub(":(k\s|kind\s)","@kind ", txt_shell)
        txt_shell = re.sub(":(t\s|type\s)","@type ", txt_shell)
        txt_shell = re.sub("@(i\s|info\s)",":i ", txt_shell)
        txt_shell = txt_shell.replace('“','"')
        txt_shell = txt_shell.replace('”','"')
        logging.info(txt_shell)

        env = os.environ
        if (re.match("@hoogle .*", txt_shell)):
            pass
        else:
            env["LC_CTYPE"] = "C"
        stdout=None
        stderr=None
        cwd = '/home/jon/fs/git/lambdabot-5.1/'


        if (re.match(":(i|info)", txt_shell)):
            p_lambdabot = subprocess.Popen(['stack','exec','ghc','--','-w', '-e',txt_shell], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, cwd=cwd)
            stdout, stderr = p_lambdabot.communicate()
            p_lambdabot.stdout.close()
        else:
            p_lambdabot = subprocess.Popen(['stack', 'exec', 'lambdabot','--','-lWARNING','-e'+txt_shell], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, cwd=cwd)
            stdout, stderr = p_lambdabot.communicate()
            p_lambdabot.stdout.close()
        
        out = stdout.decode(encoding="utf-8", errors="ignore")
        # logging.info(out)

        out_lines = out.splitlines()
        if(len(out_lines) > 25):
            out = '\n'.join(out_lines[:25]) + '\n [ +' + str(len(out_lines) - 25) + ' lines ]'

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

