import requests
from bs4 import BeautifulSoup
import operator

# Some of the most popular, regularly updated news subreddits, chosen to observe trends.
subreddits = ['news', 'worldnews', 'politics', 'worldpolitics', 'worldevents', 'futurology', 'politicaldiscussion', 'truereddit']

# Scrape a subreddit, turn code into a string, make everything lowercase, divide into individual words.
def crawl(subreddit):
    url = 'https://www.reddit.com/r/{}/'.format(subreddit)
    word_list = []
    source_code = requests.get(url).text
    soup = BeautifulSoup(source_code, "html.parser")
    
    for post_text in soup.findAll('a', {'class': 'title may-blank outbound'}):
        content = post_text.string
        words = content.lower().split()
        for each_word in words:
            word_list.append(each_word)
    
    clean_list(word_list)


# Remove unwanted symbols, add the 'cleaned up' words to list
def clean_list(word_list):
    clean_word_list = []
    for word in word_list:
        symbols = "`~!@#$%^&*()_+-={}:\">?<[];'./,"
        for i in range(0, len(symbols)):
            word = word.replace(symbols[i], "")

        stop_words = ["about", "above", "after", "again", "against", "all", "and", "any", "are", "because", "been", "before", "being",
                      "below", "between", "both", "but", "could", "did", "does", "doing", "down", "during", "each", "few", "for", "from",
                      "further", "had", "has", "have", "having", "her", "here", "hers", "herself", "him", "himself", "his", "how", "into",
                      "its", "itself", "lets", "more", "most", "myself", "nor", "once", "only", "other", "ought", "our", "ours",
                      "ourselves", "out", "over", "own", "same", "she", "should", "some", "such", "than", "that", "the", "their", "theirs",
                      "them", "themselves", "then", "there", "these", "they", "this", "those", "through", "too", "under", "until", "very",
                      "was", "were", "what", "when", "where", "which", "while", "who", "whom", "why", "with", "would", "you", "your"]
        if len(word) > 2:
            if word not in stop_words:
                clean_word_list.append(word)

    create_dictionary(clean_word_list)


# Create a dictionary with the words as keys and how many times each word is present as the values.
def create_dictionary(clean_word_list):
    word_count = {}
    for word in clean_word_list:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    # Sort dictionary in descending order.
    word_count = sorted(word_count.items(), key=operator.itemgetter(1))
    # Print out the 5 most popular words.
    most_used = word_count[-1], word_count[-2], word_count[-3], word_count[-4], word_count[-5]
    print(most_used)


# Use the word counter on the front page of every subreddit in the 'subreddits' list.
for k in range(len(subreddits)):
    try:
        print('On r/{}:'.format(subreddits[k]))
        crawl(subreddits[k])
    except IndexError:
        print('Crawler failed to get the data from the {} subreddit'.format(subreddits[k]))
