#!/usr/bin/python



################################################################################
################################################################################
from apiclient.discovery import build

def search_images(phrase,id_search,api_key,pages):
    resource = build("customsearch", 'v1', developerKey=api_key).cse();

    link=[];
    for i in range(1, pages*10, 10):
        try:
            result = resource.list(q=phrase, searchType='image', imgType='photo', cx=id_search, start=i).execute()
            
            item = result['items'];
            for j in range(len(result['items'])):
                link.append(result['items'][j]['link'])
            
            print("worked page",1+(i-1)/10)
        except:
            return link;
        
    return link;


################################################################################
################################################################################

import re
def detect_extension_from_name(filename):
    x = re.search("(.jpg).*", filename, re.IGNORECASE);
    if x:
      return '.jpg'
    x = re.search("(.jpeg).*", filename, re.IGNORECASE);
    if x:
      return '.jpg'
    x = re.search("(.png).*", filename, re.IGNORECASE);
    if x:
      return '.png'
    x = re.search("(.bmp).*", filename, re.IGNORECASE);
    if x:
      return '.bmp'
    x = re.search("(.webp).*", filename, re.IGNORECASE);
    if x:
      return '.webp'
    
    return '.unknown'


################################################################################
################################################################################
from PIL import Image
import os

# Resizes the image filename if it has width greater than min_width, or
# delete if it is lesser.
def resize_image_or_delete(filename,min_width):
    try:
        image = Image.open(filename)
        if(image.size[0]<min_width):
            os.remove(filename)
            return False;
        if(image.size[0]==min_width):
            return True;
        
        new_image = image.resize((int(min_width),int(image.size[1]*min_width/image.size[0])))
        new_image.save(filename);
        return True;
    except:
        os.remove(filename)
        return False;

################################################################################
################################################################################
import requests
import os 
import imghdr

# download all urls in 'link' list and save in 'directory', each image file 
# has the format 'prename'+int()+extension.
# All images will be resize to min_width.
def download_images_in_dir(link,directory,prename='prename',min_width=600):
    link_valid=[];
    name_valid=[];
    # Create target Directory if don't exist
    if not os.path.exists(directory):
        os.mkdir(directory)
        print("Directory " , directory ,  " Created ")
    
    k=1;
    for URL in link:
        print("\n\nsaving:"); print(URL);
        
        ext=detect_extension_from_name(URL);
        
        filename=os.path.join(directory,prename+str(k)+ext);
        print("working in:",filename);
        
        try:
            response = requests.get(URL, timeout=(5.0,27))#(conect, read)
            
            print("reason:",response.reason)
            if(response.status_code==200):
                open(filename, "wb").write(response.content)
                
                # Cambiando nombre si .unknown
                trash, ext = os.path.splitext(filename)
                if(ext==".unknown"):
                    print("file format not recognize in",filename);
                    res=imghdr.what(filename);
                    if(res!=None):
                        filename_old=filename;
                        filename=trash+"."+res;
                        print("change name to",filename)
                        os.rename(filename_old, filename);
                
                # Resize image
                res=resize_image_or_delete(filename,min_width);
                
                if(res):
                    k=k+1;
                    print(filename);
                    link_valid.append(URL);
                    name_valid.append(filename);
                else:
                    print("URL with file with width less than",min_width);
            else:
                print("URL broken :(");
        
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            #raise SystemExit(e);
            print("ERROR;pass")
    return link_valid, name_valid;

