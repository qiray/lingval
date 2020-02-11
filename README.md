# lingval

Tool for making Russian text analysis - paragraphs, sentences and words count, word clouds, dialogues percentage, sentiment and POS analysis and even more.

## Requirements

This tool uses Python 3 so you need to have Python 3 and pip for build and run it. To install them use instructions for your OS.

It also needs some extra libraries (see file [requirements.txt](requirements.txt)). Use pip to install them. For example:

``` bash
pip3 install -r requirements.txt --user
```

On some systems you should also install *python3-dev* package.

## Usage

It's a console tool. You can run it using these commands:

```bash
python main.py
#or
python3 main.py
```

Lingval has some command line attributes:

```
usage: lingval [-h] [--file FILE] [--lang LANG] [--about]

Tool for analyzing Russian fiction texts.

optional arguments:
  -h, --help   show this help message and exit
  --file FILE  File for analyze
  --lang LANG  Set locale
  --about      Show about info
```

For example to analyse file text.txt and make output in Russian run:

```bash
python main.py --file text.txt --lang ru
#or
python3 main.py --file text.txt --lang ru
```

Files must be in **UTF-8** encoding.

When completed there will be a folder named "output/text" containing these files:

- **collocations.csv** - 10 top collocations;
- **common_data.csv** - paragraphs, sentences, words and symbols count;
- **dialogues_info.csv** - dialogues percentage;
- **pos_data.csv** - POS count and percentage;
- **sentences_data.csv** - sentences count, max, average, median and mode lengths;
- **sentiments.csv** - sentiments percentage;
- **topwords_data.csv** - 20 top words;
- **longest_sentence.txt** - longest sentence;
- **words.png** - wordcloud with words;
- **lemmas.png** - wordcloud with lemmas.

## Examples

Here are some lingval results (in Russian):

- [Anna Karenina by Leo Tolstoy](examples/Karenina.md);

- [Crime and Punishment by Fyodor Dostoevsky](examples/CrimeAndPunishment.md);

- [Prisoners of Power, also known as Inhabited Island by Arkady and Boris Strugatsky](examples/InhabitedIsland.md);

- and [their comparison](examples/common.md).

## Credits

This tool uses some libs and packages:

- Yandex Mystem - tool for lemmatizing Russian texts;
- pymystem3 - Python wrapper for Yandex Mystem;
- nltk - toolkit for processing natural languages;
- dostoevsky - tool for making sentiment analysis for Russian texts;
- wordcloud - package for making word clouds;
- tabulate - package for printing tables;
- argparse - package for parsing command line args;
- stop_words - package with list of stop words.

## Contact

You are welcome to open [new issue](https://github.com/qiray/lingval/issues/new) if you have any questions, suggestions or bugs.

If you like this project you can star it [here](https://github.com/qiray/lingval).

## License

This program uses MIT license. For more information see the LICENSE file.
