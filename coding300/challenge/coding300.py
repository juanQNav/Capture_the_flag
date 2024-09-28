# recommended command
# python .\coding300.py --dir .\lvl1\lvl --fzip .\lvl1\lvl --output .\lvl1\ --lvl 1
import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pytesseract
from sudoku import Sudoku
import zipfile
import argparse
import stepic
import time

def show_img(img):
    plt.figure()
    plt.imshow(img)
    plt.axis('off')
    plt.show(block=False)
    input("Enter to continue...")
    plt.close("all")

# stack overflow
# https://stackoverflow.com/questions/11649577/how-to-invert-a-permutation-array-in-numpy
def invert_permutation(p):
    """Return an array s with which np.array_equal(arr[p][s], arr) is True.
    The array_like argument p must be some permutation of 0, 1, ..., len(p)-1.
    """
    p = np.asanyarray(p)  
    s = np.empty_like(p)
    s[p] = np.arange(p.size)
    return s
#stack overflow (based on)
#https://stackoverflow.com/questions/11930515/unzip-nested-zip-files-in-python?newreg=49500d2594314ad58e9fe63efd1b675e
def extract_zip_level(zip_path, dir, password):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dir, pwd=bytes(password, 'utf-8'))
            print(f"Level successfully extracted in {dir}")
            return True
    except RuntimeError as e:
        print(f"Error extracting ZIP: {e}")
        return False

def defint(text):
    if text == '':
        return 0
    return int(text)

def extract_puzzle_from_image(final_img, cellsize, ocr_positions=None):
    puzzle = []
    for j in range(16):
        row = []
        for i in range(16):
            if ocr_positions:
                x1, y1, x2, y2 = ocr_positions[j][i]
                prep = final_img.crop((x1, y1, x2, y2))
            else:
                prep = final_img.crop((i*cellsize+10, j*cellsize+10, (i+1)*cellsize-10, (j+1)*cellsize-10))

            row.append(defint(pytesseract.image_to_string(prep, config="--psm 7 -c tessedit_char_whitelist=0123456789 digits").strip()))
        puzzle.append(row)
    return puzzle

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", type=str, required=True, help="Img source dir")
    ap.add_argument("--fzip", type=str, required=True, help="First zip source dir")
    ap.add_argument("--lvl", type=int, required=False, help="Number of level")
    ap.add_argument("--simg", action="store_true", help="Show images")
    ap.add_argument("--output", type=str, required=True, help="Output dir")
    
    args = vars(ap.parse_args())

    img_base_path = args['dir']
    zip_base_path = args['fzip']
    simg =args['simg']
    output_path = args['output']

    lvl = args['lvl']
    inti_lvl = lvl
    ocr_positions = None

    start_time = time.time() 
    while True:
        print(f"LEVEL {lvl}")
        img_path = f"{img_base_path}{lvl}.png"
        zip_path = f"{zip_base_path}{lvl+1}.zip"
        
        if not os.path.exists(img_path):
            break

        print(f'img_path: {img_path}')
        print(f'zip_path: {zip_path}')

        img = Image.open(img_path)

        if simg:
            print("Show steganographed image\n")
            show_img(img)

        message = stepic.decode(img)
        print(f'message: {message}')

        seed = int(message.replace("#", ""))
        print(f'seed: {seed}\n')
        np.random.seed(seed)
        pix = list(img.getdata())

        indices = list(invert_permutation(np.random.permutation(len(pix))))
        newpix = [pix[indices[i]] for i in range(len(pix))]

        restored_img = Image.new('RGB', (img.width, img.height))
        restored_img.putdata(newpix)

        if simg:
            print("Show restored image\n")
            show_img(restored_img)

        height, width = img.height, img.width
        block_size = width // 4

        blocks = [None] * 16
        for i in range(4):
            for j in range(4):
                sub_img = restored_img.crop((i*block_size, j*block_size, (i+1)*block_size, (j+1)*block_size))
                val = stepic.decode(sub_img).replace("#", "")
                rot = int(val[:2], 2)
                ind = int(val[2:], 2)   
                blocks[ind] = sub_img.rotate(-90*rot)

        final_img = Image.new('RGB', (width, height))
        for i in range(16):
            final_img.paste(blocks[i], ((i%4)*block_size, (i//4)*block_size)) 

        if simg:
            print("Show final image\n")
            show_img(final_img)

        cellsize = img.width // 16

        print("processing puzzle...\n")
        if lvl == inti_lvl:
            ocr_positions = []
            for j in range(16):
                row_positions = []
                for i in range(16):
                    x1, y1, x2, y2 = i*cellsize+10, j*cellsize+10, (i+1)*cellsize-10, (j+1)*cellsize-10
                    row_positions.append((x1, y1, x2, y2))
                ocr_positions.append(row_positions)

        puzzle = extract_puzzle_from_image(final_img, cellsize, ocr_positions)

        print("Puzzle\n")
        for row in puzzle:
            print(row)

        sud = Sudoku(4, 4, board=puzzle)
        sol = sud.solve()
        print(sol)

        password = ""
        for row in sol.board:
            for val in row:
                password += str(val)

        print(f'password: {password}\n')

        if not extract_zip_level(zip_path, output_path, password):
            print("No more levels to extract or incorrect password.\n")
            break  
        
        lvl += 1
        print("--"*35)

    end_time = time.time()  
    elapsed_time = end_time - start_time 
    print(f"Process completed in {elapsed_time:.2f} seconds.")