# _*_ coding=utf-8 _*_
import base64
import cmd
from encodings import aliases
import os
import shutil
import subprocess
import re
from time import time
import requests
from requests.exceptions import ReadTimeout


class SvnRbClient(cmd.Cmd):
    def __init__(self, completekey='tab', stdin=None, stdout=None):
        cmd.Cmd.__init__(self, completekey, stdin, stdout)
        # read .reviewboardrc file as configuration
        self.rb_configuration = '.reviewboardrc'
        self.rb_url = '192.168.3.180'
        self.encoding = sys.getfilesystemencoding()
        self.svn_diff_command = 'svn diff '
        self.svn_status_xml = 'svn status --xml'
        self.svn_status = 'svn status '
        self.svn_add = 'svn add '
        self.svn_commit = 'svn commit %s --message "review:%s %s"'
        self.temp_diff_file = 'differ_temp' + os.path.sep + 'temp_differ_file.txt'
        self.rb_post = "rbt post --diff-filename %s --target-people %s --summary %s --description %s "
        self.rb_post_w_rrId = "rbt post -r %s"
        self.rb_publish = "rbt publish -r %s"

        self.init_configuration()
        self.rb_requests = RbRequests(self.rb_username, self.rb_password, self.repository_name)
        SVNRBTLogs.create_default_differ_temp_folder()
        self.svn_logger = SVNRBTLogs()
        #self.ignore_folders = self.get_ignore_folders()
        if os.path.isfile(self.temp_diff_file):
            os.remove(self.temp_diff_file)

    intro = '''
        Review Board Client, ? for help, and following is the command lists:
        |ID | command : comments
        1. setup:setup review board setting
        2. pre:precommit your changes to review board
        3. upre:update your precommit
        4. ss:svn status,find svn status for the working copies
        5. sa:svn add,add files to local svn
        6. sd:svn delete,delete svn file
        7. ci:svn commit,commit the changes by review request id
        8. sre: revert changes
        9. sdiff: generate differ file
        10.sci: commit the selected files directly
        11. exit: exit the client
        12.su: update svn
    '''

    prompt = '(ReviewBoard Client)'

    def do_setup(self, arg):
        """
        set up review board setting
        :param arg:
        :return:
        """
        print "setup reviewboard configuration:"
        prompt = "<"
        print "please input your Review Board ID/  Employee ID:"
        self.rb_username = self.encode_input(raw_input(prompt))
        print "Your review board ID %s" % (self.decode_for_output(self.rb_username))
        print "please input your Review Board password："
        self.rb_password = self.encode_input(raw_input(prompt))
        print "your review board password:%s" % (self.decode_for_output(self.rb_password))
        print "please input your default reviewer employee ID:"
        self.rb_audit_user = self.encode_input(raw_input(prompt))
        print "Default Review Employee ID:%s" % (self.decode_for_output(self.rb_audit_user))

        rbt_setup_repo_cmd = 'rbt setup-repo --server %s --username %s --password %s' % (
            self.rb_url, self.rb_username, self.rb_password)
        print rbt_setup_repo_cmd
        subprocess.call(rbt_setup_repo_cmd, shell=True)
        with open(self.rb_configuration, mode='w') as f:
            f.write("USERNAME=%s" % self.rb_username)
            f.write("\n")
            f.write("PASSWORD=\"%s\"" % self.rb_password)
            f.write('\n')
            f.write("TARGET_PEOPLE=%s" % self.rb_audit_user)
            f.write('\n')
            f.write("OPEN_BROWSER=True")
        self.init_configuration()

    def do_ss(self, arg):
        """
        same as svn status, just change the output
        :param arg:
        :return:
        """
        self.get_changed_files()

    def do_su(self,args):
        subprocess.call('svn update',shell=True)

    def do_sci(self,line):
        """
        commit files directly
        :return:
        """
        file_list = self.select_svn_changed_files()
        if len(file_list[0]) > 0:
            subprocess.call(self.svn_add + file_list[0], shell=True)
        # todo add delete file handler
        prompt = "Please input summary for your changes,it is nice to provide your Bug No:>"
        summary = self.encode_input(raw_input(prompt))
        ci_command = 'svn commit %s -m "%s"'% (file_list[1],summary)
        ci_command = ci_command.replace('\n', '')
        print ci_command.encode(self.encoding)
        # subprocess.call(['svn','commit',rr_notes[str(item)]['changed_file_lists'].replace("\"",""),'-m',log])
        subprocess.call(ci_command.encode(self.encoding), shell=True)

    def do_pre(self, arg):
        """
        pre-commit changes to review board,the steps:
        # get all changed file lists
        # pass selected file to generate diff files
        # prompt summary,description,target reviewer for issues a review request draft
        # rbt post --summary %s --description %s --open_browser True --diff-filename=
        # rbt publish:publish draft review request
        # rbt get request id, and move the diff file to a folder which named as the request id
        # also create the review requests notes file
        :param arg: None args passed, leave for parsing
        :return:
        """

        print "pre-commit the changes"
        # list all the status
        submitted_file_list = self.pre_precommit()

        print submitted_file_list + " is ready to post to review board......"
        # process rbt post to submit review request
        prompt = "Please input your reviewer ID,Entry for default Reviewer> "
        target_people = self.encode_input(raw_input(prompt))
        print "reviewer ID: " + target_people
        if len(target_people) == 0:
            target_people = self.rb_audit_user

        prompt = "Please input summary for your changes,it is nice to provide your Bug No:>"
        summary = self.encode_input(raw_input(prompt))
        # prompt = "Please input detail description for your changes, Enter for use Summary as your detail description:"
        description = self.encode_input(summary)
        # if len(description) == 0:
        # description = summary

        try:
            rr_id = self.rb_requests.create_rr(summary, description, target_people, self.temp_diff_file)
            print 'draft request review id :' + str(rr_id)
            # create request review notes
            rr_dir = self.svn_logger.create_svn_rbt_notes(rr_id, summary, description, target_people,
                                                          submitted_file_list)
            shutil.move(self.temp_diff_file, rr_dir + os.path.sep + 'diff_' + str(rr_id) + '_latest.txt')
        finally:
            if os.path.isfile(self.temp_diff_file):
                os.remove(self.temp_diff_file)

    def do_upre(self, args):
        """
        update pre-commit request review with new differ file
        :param args:
        :return:
        """
        rr_id, rr_notes = self.select_review_request()
        submitted_file_list = self.pre_precommit()
        self.rb_requests.upload_differ_file_by_request(rr_id, self.temp_diff_file)
        configuration = self.svn_logger.get_rr_log(rr_id)
        self.rb_requests.publish_rr(rr_id, {'public': True})

        try:
            print 'update request review id :' + str(rr_id)
            # create request review notes
            rr_dir = self.svn_logger.create_svn_rbt_notes(rr_id, configuration['summary'], configuration['description'],
                                                          configuration['target_people'], submitted_file_list)
            shutil.move(rr_dir + os.path.sep + 'diff_' + str(rr_id) + '_latest.txt',
                        rr_dir + os.path.sep + 'differ_' + str(time()) + '.txt')
            shutil.move(self.temp_diff_file, rr_dir + os.path.sep + 'diff_' + str(rr_id) + '_latest.txt')
        finally:
            if os.path.isfile(self.temp_diff_file):
                os.remove(self.temp_diff_file)

    def do_sa(self,args):
        """
        add files to local svn
        :return:
        """
        print "Add files to SVN"
        file_list = self.select_svn_changed_files()[0]
        print "adding files for:" + file_list[0]
        if len(file_list[0]) > 0:
            subprocess.call(self.svn_add + file_list[0], shell=True)

    def do_sdiff(self, arg):
        """
        generate diff file
        :param arg:
        :return:
        """
        self.pre_precommit()

    def do_sre(self, args):
        """
        revert selected files' last changes
        :param args:
        :return:
        """
        print "revert changes"
        files_lists = self.select_svn_changed_files()[1]
        subprocess.call("svn revert %s --depth infinity" % files_lists, shell=True)

    def select_review_request(self):
        rr_notes = self.svn_logger.retrieve_rb_rr_notes()
        print 'last 5 review requests status:'
        print 'Request Review Id |Summary  | Status | Changed File List '
        for key in rr_notes:
            output_note = rr_notes[key]['summary']
            file_list = rr_notes[key]['changed_file_lists']
            status = self.rb_requests.get_review_request_status(key)
            print '%s | %s | %s | %s ' % (key, output_note, status, file_list)
        prompt = "please select your review request id to change:"
        prompt = self.encode_input(raw_input(prompt))
        return prompt, rr_notes


    def do_ci(self, args):
        """
        commit files based review request id
        :param args:
        :return:
        """
        prompt, rr_notes = self.select_review_request()
        if prompt == None or len(prompt) == 0: return

        for item in prompt.split(','):
            try:
                log = rr_notes[str(item)]['summary']
            except KeyError:
                print "please check your input request review it ,it is not correct,id=" + item
                return
            ci_command = self.svn_commit % (rr_notes[str(item)]['changed_file_lists'].replace('\"', ''), item, log)
            ci_command = ci_command.replace('\n', '')
            print ci_command.encode(self.encoding)
            # subprocess.call(['svn','commit',rr_notes[str(item)]['changed_file_lists'].replace("\"",""),'-m',log])
            subprocess.call(ci_command.encode(self.encoding), shell=True)

    def do_help(self, arg):
        """
        help
        :param arg:
        :return:
        """
        print self.intro

    def do_exit(self, arg):
        return -1

    def encode_input(self, input):
        return input.decode(self.encoding).encode('utf-8')

    def decode_for_output(self, output):
        return output.decode('utf-8').encode('utf-8')

    def select_svn_changed_files(self):
        parsed_changed_list = self.get_changed_files()
        print "Please select the files IDs which your want to commit,eg. 0,1,2,3, or Enter for All Files"
        prompt = "<"
        selected_file_index = raw_input(prompt)

        return self.get_selected_files(parsed_changed_list, selected_file_index)


    def init_configuration(self):
        configurations = self.parse_rb_config_file()
        try:
            self.rb_audit_user = configurations['TARGET_PEOPLE']
            self.rb_username = configurations['username'.upper()]
            self.rb_password = configurations['password'.upper()]
            self.repository_name = configurations['REPOSITORY']
        except KeyError:
            print "setup is not completed,need to run setup manually,change the .reviewboardrc"
            exit(-1)

    def pre_precommit(self):
        """
        处理新加的文件，同时生成所有的diff文件
        :param changed_file_list: 解析好的所有文件列表
        :param post_file_index:需要提交的文件序号，默认是None,表示提交所有文件
        :return:
        """
        file_tuple = self.select_svn_changed_files()
        # 添加新的文件到svn
        if len(file_tuple[0]) > 0:
            subprocess.call(self.svn_add + file_tuple[0], shell=True)
        self.generate_differ_file(file_tuple[1])
        return file_tuple[1]

    def generate_differ_file(self, changed_files):
        """
        生成的文件的differ文件
        :param changed_files:
        :return:
        """
        # svn diff <changed files> >> <file_name>
        if os.path.exists(self.temp_diff_file):
            os.remove(self.temp_diff_file)
        diff_command = self.svn_diff_command + changed_files + ' >>' + self.temp_diff_file
        # process diff file
        subprocess.call(diff_command, shell=True)

    def get_selected_files(self, changed_file_list, selected_file_index=None):
        """
        返回需要添加到SVN的列表和提交precommit review的文件列表
        :param changed_file_list: 所有改变的文件
        :param selected_file_index: 选中的文件IDs
        :return:(需要增加的文件列表，所有选中的文件）元组
        """

        file_list_to_add = ""
        post_file_name_list = ""
        # todo need to handle delete file
        #file_list_to_delete =""
        if selected_file_index is None or len(selected_file_index) == 0:
            file_list_to_add = " ".join([item[1] for item in changed_file_list if (item[0] == "?")])
            #file_list_to_delete=" ".join([item[1] for item in changed_file_list if (item[0]=="!")])
            post_file_name_list = " ".join(item[1] for item in changed_file_list)
        else:
            raw_indexes = selected_file_index.split(",")
            # to parse x-x format
            indexes = []
            for item in raw_indexes:
                if item.find('-') >= 1:
                    start, end = item.split('-')
                    indexes = indexes + [str(x) for x in range(int(start), int(end) + 1)]
                else:
                    indexes.append(item)
            # process normal
            file_list_to_add = " ".join(
                [changed_file_list[int(index)][1] for index in indexes if (changed_file_list[int(index)][0] == "?")])
            post_file_name_list = " ".join([changed_file_list[int(index)][1] for index in indexes])

        return file_list_to_add, post_file_name_list

    def get_ignore_folders(self):
        config = self.svn_logger.get_configuration('.ignorerc')
        return config['folders'].split(',')

    def parse_rb_config_file(self):
        """
        parse a .reviewboardrc file
        :return:
        """
        config = {
            'TREES': {},
            'ALIASES': {}
        }

        try:
            with open(self.rb_configuration) as f:
                exec (compile(f.read(), self.rb_configuration, 'exec'), config)
                return config
        except IOError:
            print "review board configuration is not correct,please configure it again:"
            self.do_setup(arg=None)
        finally:
            pass

    def get_changed_files(self):
        """
        返回SVN本地所有改变了的文件，返回格式为：
        ID | File SVN Status | File Name/File Path
        :return:
        """
        print "svn status:"
        return_content = subprocess.Popen(self.svn_status, shell=True, stdout=subprocess.PIPE)
        result = return_content.communicate()
        # list all the status
        changed_file = result[0].split("\n")
        parsed_changed_file = []
        print "Changed Files Status:"
        print "ID |FILE SVN Status|File Name/File Path "
        for i in range(len(changed_file)):
            # ，替换所有的空格
            changed_item = re.sub(' +', ",", changed_file[i]).split(",")
            if len(changed_item) > 1:
                # if self.is_not_ignore(changed_item[1]):
                    if not (changed_item[1].find('differ_temp')>=0 or changed_item[1].find('/target/')>=0 or changed_item[1].find('git')>=0  or changed_item[1].find('idea')>=0):
                        parsed_changed_file.append(changed_item)
        for i in range(len(parsed_changed_file)):
            print "%s | %s | %s" % (i, parsed_changed_file[i][0], parsed_changed_file[i][1])
        return parsed_changed_file

    def is_not_ignore(self, file_path):
        flag= True
        if len(self.ignore_folders)==0: 
            return True
        for item in self.ignore_folders:
            """todo: not correct yet,just for simple functionality"""
            if file_path.upper().find(item.upper()) >= 0:
                flag=False

        return flag


class SVNRBTLogs():
    def __init__(self):
        pass

    BASE_DIFFER_PATH = 'differ_temp'
    DIFF_FILE = 'temp_differ.txt'
    NOTES_FILE = 'notes.txt'

    @staticmethod
    def create_dir(dirPath):
        dirs = dirPath.split(os.path.sep)
        temp = ""
        for i in range(len(dirs)):
            temp = temp + dirs[i] + os.path.sep
            if not os.path.exists(temp):
                os.mkdir(temp)

    @staticmethod
    def create_default_differ_temp_folder():
        SVNRBTLogs.create_dir(SVNRBTLogs.BASE_DIFFER_PATH)

    def create_svn_rr_folder(self, rr_id):
        """
        根据review request id 创建review request log 目录，此目录放置此次更新的review request 的描述，更新的文件列表
        以及不同的diff文件
        :param rr_id:
        :return:
        """
        rr_path = SVNRBTLogs.BASE_DIFFER_PATH + os.path.sep + str(rr_id)
        # create review request id folder
        self.create_dir(rr_path)
        return rr_path

    def move_differ_file(self, rr_id):
        """
        移动临时的diff 文件到temp 目录
        :param rr_id:
        :return:
        """
        rr_diff_path = self.create_svn_rr_folder(rr_id)
        shutil.move(SVNRBTLogs.BASE_DIFFER_PATH + os.path.sep + SVNRBTLogs.DIFF_FILE,
                    rr_diff_path)

    def create_svn_rbt_notes(self, review_request_id, summary, description, target_user, file_list):
        """
        创建request review的记录
        :param review_request_id:
        :param summary:
        :param description:
        :param target_user:
        :param file_list:
        :return:
        """
        rr_dir = self.create_svn_rr_folder(review_request_id)
        rr_note = rr_dir + os.path.sep + SVNRBTLogs.NOTES_FILE
        notes = {}
        if os.path.exists(rr_note):
            with open(rr_note, 'r+') as f:
                exec (compile(f.read(), rr_note, 'exec'), notes)
                try:
                    new_file_list = ' '.join(
                        set(notes['changed_file_lists'].split(' ') + file_list.split(' ')))
                    self.write_to_note(rr_note, review_request_id, summary, description, new_file_list, target_user)

                except KeyError:
                    self.write_to_note(rr_note, review_request_id, summary, description, file_list, target_user)
        else:
            self.write_to_note(rr_note, review_request_id, summary, description, file_list, target_user)
        return rr_dir

    @staticmethod
    def write_to_note(rr_note, review_request_id, summary, description, file_lists, target_user):
        notes = {}
        with open(rr_note, 'w') as f:
            notes['review_request_id'] = review_request_id
            notes['summary'] = summary
            notes['description'] = description
            notes['changed_file_lists'] = file_lists.strip().replace('\r', ' ')
            notes['target_people'] = target_user
            for key in notes:
                log = '%s=%s\n' % (key, notes[key])
                f.write(log.encode('utf-8'))
                f.write('\n')

    def retrieve_rb_rr_notes(self):

        dirs = os.listdir(self.BASE_DIFFER_PATH)
        # fetch latest 5 files
        dirs = sorted(dirs, cmp=lambda x, y: int(y) - int(x))[:5]
        rr_notes = {}
        for item in dirs:
            # get status
            rr_notes[item] = self.get_rr_log(item)

        return rr_notes

    def get_configuration(self, path):
        configuration = {}
        try:
            with open(path, 'r+') as f:
                lines = f.readlines()
                for t1 in [line for line in lines if line != '\n']:
                    kv = t1.split('=')
                    configuration[kv[0]] = kv[1].replace("\"", '')
        except:
            pass
        return configuration

    def get_rr_log(self, rr_id):
        '''
        only get the configuration from the review reqest note file
        :param item:
        :return:
        '''
        path = SVNRBTLogs.BASE_DIFFER_PATH + os.path.sep + str(rr_id) + os.path.sep + self.NOTES_FILE
        # path = SVNRBTLogs.BASE_DIFFER_PATH + os.path.sep + item+ os.path.sep + item+'.txt'
        return self.get_configuration(path)


class RbRequests():
    def __init__(self, username, password, repository_name):
        self.username = username
        self.password = password
        self.auth_codes = 'Basic ' + base64.b64encode(str(username) + ':' + password)
        self.repository_name = repository_name
        self.default_headers = {'Authorization': self.auth_codes,
                                'Content-type': 'application/json',
                                "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3"
            , "Accept-Encoding": "gzip,deflate"
            , "Content-Type": "text/plaint-text; charset=utf-8"}
        self.get_repository_id()

    def get_repository_id(self):
        repository_url = 'http://192.168.3.180/api/repositories/?start=0&max-results=200'
        r = requests.get(repository_url, headers=self.default_headers, data={'name': self.repository_name})
        try:
            for item in r.json()['repositories']:
                if item.get('name') == self.repository_name:
                    self.repository_id = item['id']
                    self.base_directory = item['path'] + '/' + self.repository_name
                    return item['id']
            raise Exception(self.repository_name + " is not repository found")
        except Exception:
            print "review board server is down........."
            print "reason:" + r.reason


    def create_draft_request_review(self):
        review_request_url = 'http://192.168.3.180/api/review-requests/'
        r = requests.post(review_request_url, headers=self.default_headers, data={'repository': self.repository_id})
        return r.json().get('review_request').get('id')

    def update_publish_draft_request_review(self, rr_id, summary, description, target_people, public=1):

        form = {'summary': summary,
                'description': description, 'target_people': target_people, 'public': public}
        draft_url = 'http://192.168.3.180/api/review-requests/' + str(rr_id) + '/draft/'
        try:
            r = requests.put(draft_url, headers=self.default_headers, data=form, timeout=3)
            print 'update and publish request review ' + r
        except ReadTimeout as e:
            print "update draft timeout but it doesn't matter"


    def publish_rr(self, rr_id, form):
        draft_url = 'http://192.168.3.180/api/review-requests/' + str(rr_id) + '/draft/'
        try:
            r = requests.put(draft_url, headers=self.default_headers, data=form, timeout=3)
            print 'update and publish request review ' + r
        except ReadTimeout as e:
            print "update draft timeout but it doesn't matter,the request %s is updated" % (str(rr_id))


    def upload_differ_file(self, rr_id, diff_file_name):
        svn_post_diff_command = 'rbt post -r %s --diff-filename %s' % (rr_id, diff_file_name)

        # upload_differ = 'http://192.168.3.180/api/review-requests/' + str(rr_id) + '/draft/file-attachments/'
        # files = {'path': open(diff_file_name, 'rb'), 'basedir': self.base_directory}
        # data = {'basedir': self.base_directory}
        # r = requests.post(upload_differ, data=data, files=files, headers={'Authorization': self.auth_codes},
        # timeout=1.5)

        post_rest = subprocess.Popen(svn_post_diff_command, shell=True, stdout=subprocess.PIPE).communicate()
        print 'upload differ file result: ' + post_rest[0]

    def upload_differ_file_by_request(self, rr_id, diff_file_name):

        upload_differ = 'http://192.168.3.180/api/review-requests/' + str(rr_id) + '/diffs/'

        files = {'path': open(diff_file_name, 'rb')}
        data = {'basedir': self.base_directory}
        r = requests.post(upload_differ, data=data, files=files, headers={'Authorization': self.auth_codes},
                          timeout=30)
        print r

    def create_rr(self, summary, description, target_people, diff_file_name):
        self.get_repository_id()
        rr_id = self.create_draft_request_review()
        # print self.upload_differ_file(rr_id, diff_file_name)
        print self.upload_differ_file_by_request(rr_id, diff_file_name)
        self.update_publish_draft_request_review(rr_id, summary, description,
                                                 target_people)
        return rr_id

    def get_review_request_status(self, rr_id):
        review_request_url = 'http://192.168.3.180/api/review-requests/' + str(rr_id) + '/'
        r = requests.get(review_request_url, headers=self.default_headers)
        return r.json().get('review_request').get('status')


if __name__ == '__main__':
    import sys

    reload(sys)
    sys.setdefaultencoding('utf8')
    aliases.aliases['cp65001'] = 'utf-8'
    SvnRbClient().cmdloop()
