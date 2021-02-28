import logging, os, time
from logging.handlers import RotatingFileHandler


from rich.console import Console
from rich.theme import Theme

from hytest.product import version



os.makedirs('log',exist_ok=True)

# 日志文件
logger = logging.getLogger('my_logger') 
logger.setLevel(logging.DEBUG)

logFile = os.path.join('log','testresult.log')
handler = RotatingFileHandler(
    logFile, 
    maxBytes=1024*1024*30, 
    backupCount=2,
    encoding='utf8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt='%(message)s')
handler.setFormatter(formatter)

handler.doRollover() # 每次启动创建一个新log文件，而不是从原来的基础上继续添加

logger.addHandler(handler)


# # 重定向stdout，改变print行为，同时写屏和日志
# import sys
# class MyPrintClass:
 
#     def __init__(self):
#         self.console = sys.stdout

#     def write(self, message):
#         self.console.write(message)
#         logger.info(message)
 
#     def flush(self):
#         self.console.flush()
#         # self.file.flush()

# sys.stdout = MyPrintClass()



console = Console(theme=Theme(inherit=False))

print = console.print


class LogLevel:
    level = 0



class Stats:
  
        
    def testStart(self,_title='Test Report'):
        self.result = {
            'case_count' : 0,
            'case_pass'  : 0,
            'case_fail'  : 0,
            'case_abort' : 0,
            'suite_setup_fail' : 0,
            'case_setup_fail' : 0,
            'suite_teardown_fail' : 0,
            'case_teardown_fail' : 0,
            'case_pass_list'  : [],
            'case_fail_list'  : [],
            'case_abort_list' : [],

        }
                
    
        self.start_time = time.time()

    def testEnd(self):
        self.end_time = time.time()
        self.test_duration = self.end_time-self.start_time

    def enter_case(self, caseId ,name, case_className):       
        self.result['case_count'] += 1    
    
    def case_pass(self, caseId, name): 
        self.result['case_pass'] += 1   
        self.result['case_pass_list'].append(caseId)   
    
    def case_fail(self, caseId, name, e, stacktrace):
        self.result['case_fail'] += 1   
        self.result['case_fail_list'].append(caseId)  
        
    
    def case_abort(self, caseId, name, e, stacktrace):
        self.result['case_abort'] += 1   
        self.result['case_abort_list'].append(caseId)  

    # utype 可能是 suite  case  case_default     
    def setup_fail(self,name, utype, e, stacktrace):  
        if utype == 'suite':
            self.result['suite_setup_fail'] += 1   
        else:
            self.result['case_setup_fail'] += 1 
    
    def teardown_fail(self,name, utype, e, stacktrace):  
        if utype == 'suite':
            self.result['suite_teardown_fail'] += 1   
        else:
            self.result['case_teardown_fail'] += 1 

stats = Stats()

class ConsoleLogger:
    
    def testEnd(self):
        ret = stats.result
        print(f'\n\n  ========= 测试耗时 : {stats.test_duration:.3f} 秒 =========\n')
        
        print(f"\n  用例数量 : {ret['case_count']}")

        print(f"\n  通过 : {ret['case_pass']}", style='green')
        
        num = ret['case_fail']
        style = 'white' if num == 0 else 'bright_red'
        print(f"\n  失败 : {num}", style=style)
        
        num = ret['case_abort']
        style = 'white' if num == 0 else 'bright_red'
        print(f"\n  异常 : {num}", style=style)
        
        num = ret['suite_setup_fail']
        style = 'white' if num == 0 else 'bright_red'
        print(f"\n  套件初始化失败 : {num}", style=style)
        
        num = ret['suite_teardown_fail']
        style = 'white' if num == 0 else 'bright_red'
        print(f"\n  套件清除  失败 : {num}", style=style)
        
        num = ret['case_setup_fail']
        style = 'white' if num == 0 else 'bright_red'
        print(f"\n  用例初始化失败 : {num}", style=style)
        
        num = ret['case_teardown_fail']
        style = 'white' if num == 0 else 'bright_red'
        print(f"\n  用例清除  失败 : {num}", style=style)

    
    def enter_suite(self,name,suitetype):   
        if suitetype == 'file' :
            print(f'\n\n>>> {name}',style='bold bright_black')

    
    def enter_case(self, caseId ,name, case_className):        
        print(f'\n* {name}',style='bright_white')

    
    def case_steps(self,name):...

    
    def case_pass(self, caseId, name):
        print('                          PASS',style='green')

    
    def case_fail(self, caseId, name, e, stacktrace):
        print(f'                          FAIL\n{e}',style='bright_red')
        
    
    def case_abort(self, caseId, name, e, stacktrace):
        print(f'                          ABORT\n{e}',style='magenta')

    
    def case_check_point(self,msg):...
            
    
    def setup(self,name, utype):...
    
    
    def teardown(self,name, utype):...

    # utype 可能是 suite  case  case_default
    def setup_fail(self,name, utype, e, stacktrace): 
        utype =  '套件' if utype == 'suite' else '用例'
        print(f'\n{utype} 初始化失败 | {name} | {e}',style='bright_red')
        # print(f'\n{utype} setup fail | {name} | {e}',style='bright_red')

    
    def teardown_fail(self,name, utype, e, stacktrace):      
        utype =  '套件' if utype == 'suite' else '用例'  
        print(f'\n{utype} 清除失败 | {name} | {e}',style='bright_red')
        # print(f'\n{utype} teardown fail | {name} | {e}',style='bright_red')

    
    def debug(self, msg):
        if LogLevel.level > 0:
            print(f'{msg}')
        

    def criticalInfo(self,msg):
        print(f'{msg}', style='bright_red')


class TextLogger:

    def testStart(self,_title=''):
        startTime = time.strftime('%Y%m%d_%H%M%S',
                                           time.localtime(stats.start_time))

        logger.info(f'\n\n  ========= 测试开始 : {startTime} =========\n')


    def testEnd(self):
        endTime = time.strftime('%Y%m%d_%H%M%S',
                                  time.localtime(stats.end_time))
        logger.info(f'\n\n  ========= 测试结束 : {endTime} =========\n')

        logger.info(f"\n  耗时    : {(stats.end_time-stats.start_time):.3f} 秒\n")
        ret = stats.result
        logger.info(f"\n  用例数量 : {ret['case_count']}")
        logger.info(f"\n  通过 : {ret['case_pass']}")
        logger.info(f"\n  失败 : {ret['case_fail']}")
        logger.info(f"\n  异常 : {ret['case_abort']}")
        logger.info(f"\n  套件初始化失败 : {ret['suite_setup_fail']}")
        logger.info(f"\n  套件清除  失败 : {ret['suite_teardown_fail']}")
        logger.info(f"\n  用例初始化失败 : {ret['case_setup_fail']}")
        logger.info(f"\n  用例清除  失败 : {ret['case_teardown_fail']}")
    
    def enter_suite(self,name,suitetype): 
        logger.info(f'\n\n>>> {name}')

    
    def enter_case(self, caseId ,name , case_className): 
        logger.info(f'\n* {name}')

    
    def case_steps(self,name):  
        logger.info(f'\n  [ case execution steps ]')

    
    def case_pass(self, caseId, name):
        logger.info('  PASS ')

    
    def case_fail(self, caseId, name, e, stacktrace):
        stacktrace = "Traceback:\n" +stacktrace.split("\n",3)[3]
        logger.info(f'  FAIL   {e} \n{stacktrace}')
        
    
    def case_abort(self, caseId, name, e, stacktrace):
        stacktrace = "Traceback:\n" +stacktrace.split("\n",3)[3]
        logger.info(f'  ABORT   {e} \n{stacktrace}')

    
    def case_check_point(self,msg):
        logger.info(f'\n-- check {msg}')
            
    
    def setup(self,name, utype): 
        logger.info(f'\n[ {utype} setup ] {name}')
    
    
    def teardown(self,name, utype): 
        logger.info(f'\n[ {utype} teardown ] {name}')

    
    def setup_fail(self,name, utype, e, stacktrace):  
        stacktrace = "Traceback:\n" +stacktrace.split("\n",3)[3]     
        logger.info(f'{utype} setup fail | {e} \n{stacktrace}')

    
    def teardown_fail(self,name, utype, e, stacktrace):  
        stacktrace = "Traceback:\n" +stacktrace.split("\n",3)[3]  
        logger.info(f'{utype} teardown fail | {e} \n{stacktrace}')

    
    def info(self, msg):        
        logger.info(msg)

    def debug(self, msg): 
        if LogLevel.level > 0:
            logger.debug(msg)

    def step(self,stepNo,desc):
        logger.info(f'\n-- 第 {stepNo} 步 -- {desc} \n')  

    def checkpoint_pass(self, desc):
        logger.info(f'\n** 检查点 **  {desc} ---->  通过\n')
        
    def checkpoint_fail(self, desc):
        logger.info(f'\n** 检查点 **  {desc} ---->  !! 不通过!!\n')    

    def criticalInfo(self,msg):
        logger.info(f'!!! {msg} !!!')


from dominate.tags import *
from dominate.util import raw
from dominate import document

class HtmlLogger:   
        
    def testStart(self,_title=''):
        # css file
        with open(os.path.join(os.path.dirname(__file__) , 'report.css'), encoding='utf8') as f:
            _css_style = f.read()
        # js file
        with open(os.path.join(os.path.dirname(__file__) , 'report.js'), encoding='utf8') as f:
            _js = f.read()


        self.doc = document(title=f'测试报告')
        self.doc.head.add(
                        meta(charset="UTF-8"),
                        style(raw(_css_style)),
                        script(raw(_js), type='text/javascript'))

        self.main = self.doc.body.add(div(_class='main_section'))

        self.main.add(h1(f'测试报告 - hytest v{version}', style='font-family: auto'))
        _, self.stats = self.main.add(h3(f'统计结果'), table(_class='result_stats'))
        _, self.logDiv = self.main.add(
            div(
                # span('切换到精简模式',_class='h3_button', id='display_mode' ,onclick="toggle_folder_all_cases()"), 
                h3('执行日志',style='display:inline'), 
                style='margin-top:2em'
            ),
            div(_class='exec_log')
        )

        # 查看上一个和下一个错误的 
        self.ev = div(
                div('∧', _class = 'menu-item', onclick="previous_error()", title='上一个错误'), 
                div('∨', _class = 'menu-item', onclick="next_error()", title='下一个错误'),
                _class = 'error_jumper'
            )
         
         
        self.main.add(div(
            div('页首', _class = 'menu-item',
                onclick='document.querySelector("body").scrollIntoView()'),
            div('教程', _class = 'menu-item', onclick='window.open("http://www.python3.vip", "_blank"); '),
            div('精简',_class='menu-item', id='display_mode' ,onclick="toggle_folder_all_cases()"),
            self.ev,
            id='float_menu')
        )

        self.curEle = self.main  # 记录当前所在的 html element
        self.curSuiteEle = None   # 记录当前的套件元素
        self.curCaseEle = None   # 记录当前的用例元素
        self.curCaseLableEle = None   # 记录当前的用例里面的 种类标题元素
        self.curSetupEle = None   # 记录当前的初始化元素
        self.curTeardownEle = None   # 记录当前的清除元素
        self.suitepath2element = {}

    
    def testEnd(self):

        execStartTime = time.strftime('%Y%m%d %H:%M:%S',
                                           time.localtime(stats.start_time))
        execEndTime = time.strftime('%Y%m%d %H:%M:%S',
                                           time.localtime(stats.end_time))

        ret = stats.result

        errorNum = 0

        trs = []
        trs.append(tr(td('开始时间'), td(f'{execStartTime}')))
        trs.append(tr(td('结束时间'), td(f'{execEndTime}')))

        trs.append(tr(td('耗时'), td(f'{stats.test_duration:.3f} 秒')))
        
        trs.append(tr(td('用例数量'), td(f"{ret['case_count']}")))

        trs.append(tr(td('通过'), td(f"{ret['case_pass']}")))
        
        num = ret['case_fail']
        style = '' if num == 0 else 'color:red'
        trs.append(tr(td('失败'), td(f"{num}", style=style)))
        errorNum += num
        
        num = ret['case_abort']
        style = '' if num == 0 else 'color:red'
        trs.append(tr(td('异常'), td(f"{num}", style=style)))
        errorNum += num
        
        num = ret['suite_setup_fail']
        style = '' if num == 0 else 'color:red'
        trs.append(tr(td('套件初始化失败'), td(f"{num}", style=style)))
        errorNum += num
        
        num = ret['suite_teardown_fail']
        style = '' if num == 0 else 'color:red'
        trs.append(tr(td('套件清除失败'), td(f"{num}", style=style)))
        errorNum += num
        
        num = ret['case_setup_fail']
        style = '' if num == 0 else 'color:red'
        trs.append(tr(td('用例初始化失败'), td(f"{num}", style=style)))
        errorNum += num
        
        num = ret['case_teardown_fail']
        style = '' if num == 0 else 'color:red'
        trs.append(tr(td('用例清除失败'), td(f"{num}", style=style)))
        errorNum += num

        self.ev['display'] = 'none' if errorNum==0 else 'block'

        # 添加统计结果
        self.stats.add(tbody(*trs))

        # 产生文件
        htmlcontent = self.doc.render()

        timestamp = time.strftime('%Y%m%d_%H%M%S',time.localtime(stats.start_time))
        reportFile = os.path.join('log',f'log_{timestamp}.html')
        with open(reportFile,'w',encoding='utf8') as f:
            f.write(htmlcontent)

        try:
            # windows
            os.startfile(reportFile)
        except:
            try:
                # mac
                os.system(f'open {reportFile}')
            except:...


    # def _findParentSuite(self,name):
    #     if name.endswith(os.path.sep):
    #         name = name[:-1]
        
    #     parentpath = os.path.dirname(name)

    #     # name 对应的 是用例根目录, 
    #     if  parentpath == '': 
    #         self._addSuiteDir(self.body,name)
    #         return None
        
    #     # rug 
    #     if parentpath not in self.suitepath2element:
    #         dirToCreate = []
    #         levels = parentpath.split(os.sep)
    #         cur = ''
    #         for level in levels:
    #             cur = os.path.join(cur,level)
            

    
    def enter_suite(self,name:str,suitetype): 
        _class = 'suite_'+suitetype

        enterInfo = '进入目录' if suitetype == 'dir' else '进入文件'
        self.curEle = self.logDiv.add(
            div(                
                div(
                    span(enterInfo,_class='label'),
                    span(name)
                ),         
                _class=_class, id=f'{_class} {name}'
            )
        )
        self.curSuiteEle = self.curEle
        self.curSuiteFilePath = name

        self.suitepath2element[name] = self.curEle
             
    
    def enter_case(self, caseId ,name, case_className):       
        # 执行有结果后，要修改这个 self.curCaseLableEle ，比如 加上 PASS
        self.curCaseLableEle = span('用例',_class='label caselabel')       

        # folder_body 是折叠区 内容部分，可以隐藏
        self.curCaseBodyEle = div(
            span(f'{self.curSuiteFilePath}::{case_className}', _class='case_class_path') , 
            _class='folder_body')
        self.curCaseEle = self.curSuiteEle.add(
            div(
                div(
                    self.curCaseLableEle,
                    span(name, _class='casename'),
                    _class='folder_header'
                ),
                self.curCaseBodyEle ,
                _class='case',id=f'case_{caseId:08}'
               )
        )
        self.curEle = self.curCaseBodyEle

    
    def case_steps(self,name):          
        ele = div(
            span('测试步骤',_class='label'), 
            _class='test_steps',id='test_steps '+name)        
        self.curEle = self.curCaseBodyEle.add(ele)

    
    def case_pass(self, caseId, name): 
        self.curCaseEle['class'] += ' pass'
        self.curCaseLableEle += ' PASS'
    
    def case_fail(self, caseId, name, e, stacktrace):
        
        self.curCaseEle['class'] += ' fail'
        self.curCaseLableEle += ' FAIL'

        stacktrace = "Traceback:\n" +stacktrace.split("\n",3)[3]
        self.curEle += div(f'{e} \n{stacktrace}', _class='info error-info')
        
    
    def case_abort(self, caseId, name, e, stacktrace):
        
        self.curCaseEle['class'] += ' abort'
        self.curCaseLableEle += ' ABORT'

        stacktrace = "Traceback:\n" +stacktrace.split("\n",3)[3]
        self.curEle += div(f'{e} \n{stacktrace}', _class='info error-info')

    
    def case_check_point(self,msg):
        pass
            
    # utype 可能是 suite  case  case_default
    def setup(self,name, utype): 

        _class = f'{utype}_setup setup'
                     
        # 套件 setup
        if utype == 'suite':
            
            # folder_body 是折叠区 内容部分，可以隐藏
            stHeaderEle = div(
                span('套件初始化',_class='label'),
                span(name),
                _class='folder_header')
            
            stBodyEle = self.curEle = div(_class='folder_body')
            
            self.curSetupEle = div(
                stHeaderEle,
                stBodyEle,
                _class=_class,
                id=f'{_class} {name}')   

            self.curSuiteEle.add(self.curSetupEle)  

        # 用例 setup
        else:
            
            self.curSetupEle = self.curEle = div(
                span('用例初始化',_class='label'),
                _class=_class,
                id=f'{_class} {name}')   

            self.curCaseBodyEle.add(self.curSetupEle)
            self.curEle['class'] += ' case_st_lable'
    
        
    # utype 可能是 suite  case  case_default
    def teardown(self,name, utype): 

        _class = f'{utype}_teardown teardown'

        # 套件 teardown
        if utype == 'suite':    
            
            # folder_body 是折叠区 内容部分，可以隐藏
            stHeaderEle = div(
                span('套件清除',_class='label'),
                span(name),
                _class='folder_header')
            
            stBodyEle = self.curEle = div(_class='folder_body')
            
            self.curTeardownEle = div(
                stHeaderEle,
                stBodyEle,
                _class=_class,
                id=f'{_class} {name}')   

            self.curSuiteEle.add(self.curTeardownEle)

        # 用例 teardown
        else:            
            self.curTeardownEle = self.curEle = div(
                span('用例清除',_class='label'),            
                _class=_class,
                id=f'{_class} {name}')       

            self.curCaseBodyEle.add(self.curTeardownEle)
            self.curEle['class'] += ' case_st_lable'


    
    def setup_fail(self,name, utype, e, stacktrace):  
        self.curSetupEle['class'] += ' fail'

        stacktrace = "Traceback:\n" +stacktrace.split("\n",3)[3]
        self.curEle += div(f'{utype} setup fail | {e} \n{stacktrace}', _class='info error-info')
    
    def teardown_fail(self,name, utype, e, stacktrace):           
        self.curTeardownEle['class'] += ' fail'

        stacktrace = "Traceback:\n" +stacktrace.split("\n",3)[3]
        self.curEle += div(f'{utype} teardown fail | {e} \n{stacktrace}', _class='info error-info')

    def info(self, msg):        
        self.curEle += div(msg, _class='info')


    def step(self,stepNo,desc):
        self.curEle += div(span(f'第 {stepNo} 步', _class='tag'), span(desc), _class='case_step')

    def checkpoint_pass(self, desc):
        self.curEle += div(span(f'检查点 PASS', _class='tag'), span(desc), _class='checkpoint_pass')
        
    def checkpoint_fail(self, desc):
        self.curEle += div(span(f'检查点 FAIL', _class='tag'), span(desc), _class='checkpoint_fail')
    
from .signal import signal

signal.register([
    stats,
    ConsoleLogger(), 
    TextLogger(), 
    HtmlLogger()])


