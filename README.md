# Pretty printed LanguageTool cli report

[LanguageTool](https://languagetool.org/?force_language=1) is a great service to find and correct grammatical errors and spelling mistakes.   
It's open source, has a free plan and also comes as a CLI that can run locally.  
Althougth the command's output is detailed and complete, it lacks colors and a simpler display.  
This project uses [Rich](https://github.com/Textualize/rich) to print [LanguageTool](https://github.com/languagetool-org/languagetool) command line report into a simple table with colors.

Use it to check the errors on your text using LanguageTool in the terminal and locally.

## Dependencies:
- python > 3.12
- Rich
- Typer
- python-docx

## Installation

<details>
<summary>Windows users</summary>
To install languagetool on Windows, please follow the instructions on the <a href="https://github.com/languagetool-org/languagetool?tab=readme-ov-file">languagetool README.</a><br>
languagetool is build in java, and you'll probably need to get:
<ul>
  <li>java 8 or later</li>
  <li><a href="https://internal1.languagetool.org/snapshots/">languagetool snapshots</a></li>
</ul>
</details>


1. Install [**uv**](https://docs.astral.sh/uv/):

macOS: Homebrew
```sh
brew install uv 
```
Unix:
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```
 
2. Install [languagetool](https://github.com/languagetool-org/languagetool?tab=readme-ov-file):

macOS: Homebrew
```sh
brew install languagetool
```

Unix:
```sh
curl -L https://raw.githubusercontent.com/languagetool-org/languagetool/master/install.sh | sudo bash <options>
```
> You can see the options on [languagetool's README](https://github.com/languagetool-org/languagetool?tab=readme-ov-file)

3. Install as a tool using uv:

```sh
uv tool install git+https://github.com/CalHenry/pretty-print-languagetool.git
```
4. Use it:

```sh
pp-languagetool --help
```
5. (optional) Create an alias

```sh
echo '' >> ~/.zshrc
echo 'alias pplt="pp-languagetool"' >> ~/.zshrc
source ~/.zshrc
```

You can also use the tool without installing it:

```sh
uvx git+https://github.com/CalHenry/pretty-print-languagetool.git --help
```

Or clone the repo
```sh
git clone https://github.com/CalHenry/pretty-print-languagetool.git
cd pretty-print-languagetool
# install as a tool in development mode
uv tool install -e .
``` 

## Usage
- with a text file (plain text or .docx)

```sh
pp-languagetool -l <lang> -f <my_file.txt>
```

- using the -t option

```sh
pp-languagetool -l en-US -t "This is a baadly sppelled sentnse"
```
If you don't provide either -f or -t, you can enter text directly as stdin. Once done, exit with ctrl-D to let languagetool check the text.

Example of the table and the colors:
![Example of output](images/example.png)

## Credits

Thanks to [LanguageTool](https://languagetool.org) for the free, open source and local service ([GitHub](https://github.com/languagetool-org))

## 🛡️ License <a name="license"></a>
Project is distributed under [MIT License](https://github.com/CalHenry/pretty-print-languagetool/blob/main/LICENSE)
