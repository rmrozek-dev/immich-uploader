# immich-uploader
simple immich mass uploader written in python
the idea of the script is to allow you to automate the uploading multiple folders containing photos/images and create albums representing photos/images from each folder.

# prerequisite
- installed python3 
- script needs api key that could be generated from user panel of immich 
please reference: https://immich.app/docs/features/command-line-interface#obtain-the-api-key

Immich supports let's say flat structure we have photo/image level and albums level (photos/images could be organize in albums),
due this fact script require create root folder which contains all folders with photos/images, which will be uploaded and converted to albums

# usage
1. mkdir rootdir
2. copy to rootdir all directories which contains photos/images you need to upload (subdirs should be flat contains only files .jpeg, .jpg, not second level of subdirs)
3. put uploader.py next to rootdir
4. make config adjustment inside script (put api key, and valid address of immich instance) 
5. run python3 uploader.py ./rootdir

# compatibility 
script is compatible with api serving by immich v1.122.1


 
