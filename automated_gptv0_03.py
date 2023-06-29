print("THE APP IS STARTING \n")
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time
import re
from mailtm import Email

chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")



############################################################################
# create an email object

message_var = None

def make_new_email():
    global message_var

    message_var = None
    email = Email()

    email.register()

    return email,email.address


# email,email_address = make_new_email()
# print(email_address)


# define a listener function that assigns the message to the global variable
def listener(message):
  global message_var
  message_var = re.findall( '(?<!#)\d{6}',str(message['html']))[0]
  
############################################################################





xpaths = {"sign_in_email_txt": '/html/body/div[1]/main/div/div[2]/form/input',
          'sign_in_email_but' : '/html/body/div[1]/main/div/button[1]',
          "inp_val_code":"/html/body/div[1]/main/div/div[3]/form/input",
          "verfy_but":"/html/body/div[1]/main/div/button[2]",

          'inp_txt_gpt': "/html/body/div[1]/div[1]/div/section/div[2]/div/div/footer/div/div/div/textarea",
          'inp_but_gpt': "/html/body/div[1]/div[1]/div/section/div[2]/div/div/footer/div/div/button[2]",
          
          'close_ad':"/html/body/div[3]/div/div/div/button",
          
          "Stop_responding":'/html/body/div[1]/div[1]/div/section/div[2]/div/div/button',


          'temp_email_copy': "/html/body/main/div[2]/div/div[1]/div[1]/div/button",
          'temp_email_last_mail': "/html/body/main/div[2]/div/div[2]/div[1]/ul/li/div[1]"  ,
          'temp_email_validation_code':'/html/body/div[2]/table[1]/tbody/tr/td/div/table/tbody/tr/td/div/div/table/tbody/tr[5]/td/div',
          "temp_email_refresh":'/html/body/main/div[2]/div/div[1]/div[2]/div[2]/button/span'
         }



def click_on_element_by_xpath(d,xpath):
    "clicks on element and returns that element"
    ele = d.find_element(By.XPATH,xpath)
    ele.click()
    return ele



def start_webdriver():
    d=webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
    return d



# d2= start_webdriver()
def get_temp_email_website(d):
    d.get('https://tempmailo.com/')
    email = click_on_element_by_xpath(d,xpaths['temp_email_copy']).text
    return email



class gpt():
    driver = 0
    chat_log =[]
    name = ''
    set_up_mes = ''
    
    def __init__(self,name,type ='sage',set_up_mes = ''):
        """starts the browser and gets free account on poe.com 
        you give it the bot "type" from poe.com, currently only sage
        "name" choose a name for your bot not to mix them,
        and "set_up_mes" which is the message you tell the bot what 
        it does, you can leave it empty
        
        you have the following function in this version of gpt
        -type_in_gpt
        -is_responding
        -get_respond
        -use_gpt
        -use_gpt_chat

        check the use of each by thier description
        """

        self.name = name


        if type == 'sage':
            email,email_address = make_new_email()
            self.driver= start_webdriver()
            
            self.driver.get('https://poe.com/')
            email_box = click_on_element_by_xpath(self.driver,xpaths['sign_in_email_txt'])
            email_box.send_keys (email_address)
            time.sleep(1.5)
            
            click_on_element_by_xpath(self.driver,xpaths['sign_in_email_but'])
            for i in range(8):
                email.start(listener)
                email.stop()
                time.sleep(2)
               
                print('val_code',message_var)
                if message_var is not None:
                    break
            else:
                print("Email not found...")
                # quit()

            if set_up_mes != '':
                self.type_in_gpt(set_up_mes)




            val_code_box = click_on_element_by_xpath(self.driver,xpaths['inp_val_code'])
            val_code_box.send_keys (message_var)
            click_on_element_by_xpath(self.driver,xpaths['verfy_but'])


            time.sleep (3)
            try:
                click_on_element_by_xpath(self.driver,xpaths['close_ad'])
            except:pass

            



    def type_in_gpt(self,to_type):
        "Simple function to type in the bot and click enter"
        input_gpt= click_on_element_by_xpath(self.driver,xpaths['inp_txt_gpt'])
        input_gpt.send_keys (to_type)
        click_on_element_by_xpath(self.driver,xpaths['inp_but_gpt'])




    def is_responding(self):
        "Simple function to check if the {stop} button exists in the screen to know if the bot still typing"
        try:
            self.driver.find_element(By.XPATH,xpaths["Stop_responding"])
        except:
            return 0
        else:
            return 1
        


    def get_respond(self):
        "Simple function to copy the last respond from the bot"
        chat_messages = self.driver.find_elements(By.CLASS_NAME, "ChatMessage_messageWrapper__Zf87D")
        return chat_messages[-1].text
    
 


    def use_gpt(self,to_type):
        """Function that uses GPT API as it types in gpt and waits for the respond to finish and gets it the only function that updates chat_log"""
        self.type_in_gpt(to_type)
        print('Prompt sent')
        for i in range(100):
            time.sleep(1)
            responded = not self.is_responding()

            if responded:
                break
        respond = self.get_respond()
        self.chat_log.append([to_type,respond])
        return respond
    



    def use_gpt_chat(self,to_type_list):
        """Function that uses GPT API for full chat then returns list of responds as it types in gpt and waits for the respond to finish and gets it"""
        responses = []
        for to_type in to_type_list:
            respond = self.use_gpt(to_type)
            responses.append(respond)
        
        return responses
    



gpts = []


def create_gpts(name):
    global gpts
    gpts.append(gpt(name))

# gptt = gpt('1')


print("dddd")