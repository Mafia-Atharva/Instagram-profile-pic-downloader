import tkinter as tk
from tkinter import ttk
import os
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk

def download_pic(username):
  
    # if username=="":
    #     status.config(text="Please enter a username.")
    #     return

    file_name = f"{username}_pfp.jpg"
    #folder to save downloaded images
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
    destination_folder = os.path.join(script_dir, "downloaded images")
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    save_location = os.path.join(destination_folder, file_name)

    #send request to instagram's profile page of user
    profile_link = f"https://www.instagram.com/{username}/"
    response = requests.get(profile_link)
  
    #parse the response to search for pic
    soup = BeautifulSoup(response.content,'html.parser')
    tag = soup.find('meta',attrs={'property':'og:image'}) 
    
    pfp_url = tag['content']
    pfp_response =  requests.get(pfp_url)
    
    with open(save_location,'wb') as f:
        f.write(pfp_response.content)
        print(f"Profile picture downloaded: {username}")
        
    return save_location


def image_gui():
    username=user_input.get()
    if username=="":
        status.config(text="Please enter a username!")
        return

    try:
        image_location = download_pic(username)
        image = Image.open(image_location)
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo
        status.config(text=f"Profile picture  :  {username}")


    except:
        status.config(text="Failed to download profile picture. Is the username correct?")

            
#GUI Window 

if __name__=="__main__":
    root = tk.Tk()
    root.title("INSTAGRAM PROFILE PIC DOWNLOADER")
    root.geometry("500x500")
    root.resizable(True,True)

    user_input = ttk.Entry(root,width=79)
    user_input.grid(row=0,column=0,padx=10)
    user_input.insert(0,"Enter an instagram username")
    user_input.bind("<FocusIn>", lambda args: user_input.delete('0', 'end'))

    style=ttk.Style()
    style.configure('.TButton', font =('MS Sans Serif', 10, 'bold'),foreground = 'green')

    button = ttk.Button(root, text="Download Profile Picture", style=".TButton", command=image_gui)
    button.grid(row=1,column=0,padx=10,pady=10)

    label = ttk.Label(root, text="Downloaded Image will appear here")
    label.grid(row=3,column=0,padx=10,pady=10)

    status = ttk.Label(root, text="")
    status.grid(row=5,column=0,padx=10,pady=10)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_height = 347
    window_width = 500
    x_coordinate = int((screen_width/2) - (window_width/2))
    y_coordinate = int((screen_height/2) - (window_height/2))

    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

    root.mainloop()