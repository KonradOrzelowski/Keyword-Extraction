#%%
# from datetime import datetime

import datetime as datetime

import time as time
import random as random
import instaloader as instaloader
import pandas as pd
import re
import info_insta as info_insta

def remove_emojis(string: str) -> str:
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoji_pattern, '', string)

class InstagramPostsScraper:
    
    def __init__(self, user: str = None, password: str = None):
        self._username = user
        self._password  = password
        
        self.__instagram_session = instaloader.Instaloader()

        if(self._username is not None and self._password  is not None):
            try:
                self.__instagram_session.login(self._username, self._password )
            except Exception as e:
                print(f"Fail to log using username {self._username}: {e}")
    
    def get_profile_from_username(self, profile_name: str) -> instaloader.Profile:
        try:
            return instaloader.Profile.from_username(self.__instagram_session.context, profile_name)
        except instaloader.exceptions.ProfileNotExistsException as e:
            print(f"Error: Profile '{profile_name}' doesn't exist")
        except Exception as e:
            print(f"Error: {e}")
    
    def get_posts_from_timerange(self, username_or_profile,
                                number_of_posts: int = 20, time_range: int = 365,
                                start_time = None, end_time = None, rate_limit: int = 2):

        # Check if time_range and number_of_posts are greater than 0
        if time_range <= 0 or number_of_posts <= 0:
            raise ValueError("time_range and number_of_posts must be greater than 0")

        # Check if start_time and end_time are datetime objects
        if not isinstance(start_time, datetime.datetime) and start_time is not None:
            raise TypeError("start_time must be a datetime object")
        if not isinstance(end_time, datetime.datetime) and end_time is not None:
            raise TypeError("end_time must be a datetime object")

        # Check if start_time is before end_time
        if start_time > end_time:
            raise ValueError("start_time must be before end_time")

        # Check if username_or_profile is a string or a Profile object
        if isinstance(username_or_profile, str):
            try:
                profile = self.get_profile_from_username(username_or_profile)
            except instaloader.exceptions.ProfileNotExistsException as e:
                print(f"Error: Profile '{profile}' doesn't exist")
            except Exception as e:
                print(f"Error: {e}")
        else:
            profile = username_or_profile
            
        # Set start_time and end_time if they are None
        if end_time is None:
            end_time = datetime.datetime.now()       
        if start_time is None:
            timedelta = datetime.timedelta(days=time_range)
            start_time = end_time - timedelta

        # Get posts from the given time range
        try:
            posts = []
            for post in profile.get_posts():
                # stop if we have enough posts
                if len(posts) >= number_of_posts:
                        break
                if start_time <= post.date <= end_time:
                    
                    post_data = {'profile_name': profile.username,
                                 'date': post.date_local.strftime('%Y-%m-%d %H:%M:%S'),
                                 'content': remove_emojis(post.caption)}
                    posts.append(post_data)
                    
                    # sleep for a random time between 15 and 30 seconds
                    time.sleep(random.randint(15, 30))
            if len(posts) == 0:
                raise ValueError("No posts found in the given time range")
            else:
                return pd.DataFrame(posts)
        
        except ValueError as e:
            print(f"Error: {e}")
        except instaloader.exceptions.ProfileNotExistsException as e:
            print(f"Error: Profile '{profile}' doesn't exist")
        except Exception as e:
            print(f"Error: {e}")
#%%

def main():
    scraper = InstagramPostsScraper()
    df = scraper.get_posts_from_timerange('harrykane', number_of_posts=10, time_range=30)
    print(df.head(10))

# if __name__ == "__main__":
#     main()
