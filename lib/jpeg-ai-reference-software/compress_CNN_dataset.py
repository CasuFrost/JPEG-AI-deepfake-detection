import subprocess
import os 
import time

dataset_path = '../CNNDetection/dataset/test'

current_folder = 0
bpp_range = [12,50,100]
profile="simple"
verbose=1
force_gpu = 0
dataset_portion = 0.1 #portion of dataset to use


skip_coefficient = int(1/dataset_portion)

if force_gpu:
    force_gpu="CUDA_VISIBLE_DEVICES=0"
else:
    force_gpu=""

iter=0
total_img_number = 0
time_info=1

for root, dirs, files in os.walk(dataset_path):
    for file in files:
        if os.path.join(root).split("/")[4]=="compressed_images":
            continue
        if iter%skip_coefficient==0:
            total_img_number+=1
        iter+=1

iter=0         
avg_time_per_img = 0
total_time = 0
virgin_counter=0 #counter for the images compressed in one session
total_img_number*=len(bpp_range)
img_counter=0 #counter for the images compressed in total

for bpp in bpp_range:
    for root, dirs, files in os.walk(dataset_path):
        dirs.sort()
        files.sort()
        for file in files:
            dataset_name=root.split("/")[4]
            
            if dataset_name=="compressed_images":
                continue

            if iter%skip_coefficient==0: #skip 75% of the images
                img_counter+=1
                current_folder=os.path.join(root).split("/")[-1] #real or fake?
                
                tmp=[dataset_path,"compressed_images","bpp"+str(bpp)]+root.split("/")[4:-1]+[current_folder]
                
                folder_output_path=os.path.join(*tmp)
                file_output_path=os.path.join(folder_output_path,file)
                
                
                #folder_output_path=dataset_path+"/compressed_images/bpp"+str(bpp)+"/"+"/".join(root.split("/")[4:-1])+"/"+current_folder #path on which the image will be saved
                
                
                if os.path.exists(file_output_path): #check if the image was already compressed (checkpoint)
                    iter+=1
                    continue
               
                os.makedirs(folder_output_path, exist_ok=True)

                
                virgin_counter+=1
                

                string_cnt = str(img_counter)+"/"+str(total_img_number)
                if verbose:
                    os.system("clear")
                    print(f"BPP {bpp}")
                    if time_info:
                        print(f"Avg time for image: {round(avg_time_per_img,3)} seconds")
                        print("Estimated time left: ",round((total_img_number-img_counter)*avg_time_per_img/(60**2),3)," hours")
                    print("Encoding image",string_cnt," ["+str(round(img_counter/total_img_number*100,2))+"%]")
                start = time.time()
                
                out=subprocess.run(f"{force_gpu} python3 -m src.reco.coders.encoder {os.path.join(root, file)} ../.tmp --set_target_bpp {bpp} --cfg cfg/tools_off.json cfg/profiles/{profile}.json",text=False,shell=True,capture_output=True) #encode
                if verbose:
                    print("Decoding image",string_cnt)

                out=subprocess.run(f"{force_gpu} python3 -m src.reco.coders.decoder ../.tmp {file_output_path}",text=False,shell=True,capture_output=True) #decode
          
                end=time.time()-start
                total_time+=end
                avg_time_per_img=total_time/virgin_counter
            iter+=1