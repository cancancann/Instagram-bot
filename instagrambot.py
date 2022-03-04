from instagramUserInfo import username,password
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys
import time



class Instagram():
    def __init__(self,username,password):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages':'en,en_US'})
        self.browser = webdriver.Chrome('chromedriver.exe', chrome_options=self.browserProfile)
        self.username = username
        self.password = password
        
   
    def sigIn(self):
        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)
        usernameInput = self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input")
        passwordInput = self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input")
        usernameInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        time.sleep(3)
        passwordInput.send_keys(Keys.ENTER)

   
    def getFollowers(self,max):
        self.browser.get(f"https://www.instagram.com/{self.username}")
        time.sleep(3)
        self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/div").click()
        time.sleep(3)
        dialog = self.browser.find_element_by_css_selector("div[role=dialog] ul")
        followerCount = len(dialog.find_elements_by_css_selector("li"))

        print(f"first count : {followerCount}")

        action = webdriver.ActionChains(self.browser)

        while followerCount < max:
            dialog.click()
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(2)

            newCount = len(dialog.find_elements_by_css_selector("li"))

            if followerCount != newCount:
                followerCount = newCount
                print(f"Second count: {newCount}")
                time.sleep(3)
            else:    
                break


        followers = dialog.find_elements_by_css_selector("li")

        followerList = []
        i = 0
        for user in followers:
            link = user.find_element_by_css_selector("a").get_attribute("href") 
            followerList.append(link) 
            i+=1
            
            if i == max:
                break

        with open("followers.txt","w",encoding="utf-8") as file:
            for item in followerList:
                file.write(item + "\n")



    def followUser(self,username):
        self.browser.get("https://www.instagram.com/" + username)
        time.sleep(2)

        followButton = self.browser.find_element_by_tag_name("button")
        print(followButton.text)

        if followButton.text != "Following":
            followButton.click()
            time.sleep(2)
        else:
            print("Already being followed..")

   
    def unfollowUser(self,username):
        self.browser.get("https://instagram.com/" + username)
        time.sleep(2)

        unfollowButton = self.browser.find_element_by_tag_name("button")
        print(unfollowButton.text)
        if unfollowButton.text =="Following":
            unfollowButton.click()
            self.browser.find_element_by_xpath("//button[text()='Unfollow']").click()
            time.sleep(2)       
        else: 
            print("You are not already following..")

    def showPost(self):
        self.browser.get(f"https://www.instagram.com/{self.username}")
        post = self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[1]/a/div").click()
        
        result = post.text
        print(result)





    
        
instgrm = Instagram(username,password)



instgrm.sigIn()
instgrm.getFollowers(50)
instgrm.gonderiGoster()
instgrm.followUser("<username>")
instgrm.unfollowUser("<username>")

# list = ["<username1>","<username2>"]

# for user in list:
#     instgrm.followUser(user)
#     time.sleep(3)


