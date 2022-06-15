#!/usr/bin/python

#pip3 install --upgrade google-api-python-client

import func_extra    as func
import func_loadsave as fls
import os

# Custom search API key
api_key=fls.text_to_string('/home/fernando/custom-searchapi-key.txt');

# ID do mecanismo de pesquisa:
id_search=fls.text_to_string('/home/fernando/id-search.txt');

# List of states
state_list=['pain', 'sad', 'happy', 'anger', 'disgust', 'fear', 'surprise'];

# Number of pages
pages=50;

# Prename of download image files
prename='prename';

# Output directory
output='output'

# Minimum width
min_width=800;


# create oput directory
fls.create_directory(output);

for state in state_list:
    # Search
    phrase='patient + bed + '+state;
    
    # Name of directory
    directory=os.path.join(output,state);
    
    link=func.search_images(phrase,id_search,api_key,pages);
    raw_link_file=directory+'_links_raw.txt';
    fls.save_list_string_in(link,raw_link_file);
    
    link=fls.load_list_string_from(raw_link_file);
    link,filename=func.download_images_in_dir(link,directory,prename,min_width);
    
    fls.save_list_string_in(link    ,directory+'_links.txt');
    fls.save_list_string_in(filename,directory+'_files.txt');

