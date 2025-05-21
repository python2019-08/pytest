'''
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [ 
        {
            //### python my_script.py --input data.csv --output results.json --verbose
            "name": "Python: Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "args": [
                "--input-srt", "/home/abner/abner2/zdev/sh/story02/story_male_cn.txt",
                "--original-text", "/home/abner/abner2/zdev/sh/story02/edge-tts-input-old-dog.txt",
                "--output-srt","output-srt.srt",                
            ]
        }
    ]
}
'''
# python others/test_argparse.py --input-srt ~/abner2/zdev/sh/story02/story_male_cn.txt --original-text ~/abner2/zdev/sh/story02/edge-tts-input-old-dog.txt --output-srt output-srt.srt  
import re
import sys
from pathlib import Path

# $ python /home/abner/abner2/zdev/ai/pytest/others/test_argparse.py --input-srt a.srt  --original-text b.txt dd
# Namespace(inputSrt='a.srt', originalText='b.txt', output_srt=None, o='dd', overwrite=False)
# args.inputSrt= a.srt
# args.originalText= b.txt
# args.output_srt= None

if __name__=="__main__":
    import argparse

    parser = argparse.ArgumentParser(description='为edge-tts生成的SRT字幕恢复标点符号')
    parser.add_argument('--input-srt',     dest="inputSrt",     required=True, help='edge-tts生成的SRT文件路径')
    parser.add_argument('--original-text', dest="originalText", required=True, help='原始文本文件路径')
    parser.add_argument('--output-srt',  help='输出的SRT文件路径，默认在原文件名后加_punct')
    parser.add_argument('o',  help='输出的文件路径')
    parser.add_argument('--overwrite', action='store_true', help='是否覆盖已存在的文件')

    args = parser.parse_args()
    print(args)
    print("args.inputSrt=",args.inputSrt)
    print("args.originalText=",args.originalText)
    print("args.output_srt=",args.output_srt)

    input_srt = Path(args.inputSrt)
    original_text = Path(args.originalText)
    
    if not args.output_srt:
        output_srt = input_srt.parent / f"{input_srt.stem}_punct{input_srt.suffix}"
    else:
        output_srt = Path(args.output_srt)