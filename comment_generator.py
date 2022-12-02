import random
from nltk import ngrams
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk import FreqDist
from scrape_data import psychic
from scrape_data import skeptic


# read from subreddit data batches
def collect_data(sub):
    data_collection = []
    with open(f"{sub}_data_store.txt", 'r') as fh:
        read_file = fh.readlines()
        for i in read_file:
            data_collection.append(i)
    return data_collection

2
test_data_psychic = collect_data(psychic)
test_data_skeptic = collect_data(skeptic)


# tokenize word data

psychic_tokens = [word_tokenize(w) for w in sent_tokenize(str(test_data_psychic))]
skeptic_tokens = [word_tokenize(w) for w in sent_tokenize(str(test_data_skeptic))]

print(len(psychic_tokens))
print(len(skeptic_tokens))


# create bigrams with padding <s>, </s>


def get_bigrams(token_data):
    bigrams = [list(ngrams(i, 2, pad_left=True, pad_right=True,
                           left_pad_symbol='<s>', right_pad_symbol='</s>')) for i in token_data]
    output = [j for i in bigrams for j in i]
    return output


bigrams_psychic = get_bigrams(psychic_tokens)
bigrams_skeptic = get_bigrams(skeptic_tokens)



# take out values that contain only alpha characters

#def filter_bigrams(bigram_data):
  #  filtered_bigrams = []
   # for i in bigram_data:
   #     for j in i:
   #         if j.isalpha() and ('\\n' or '\\n ') not in j:
   #             filtered_bigrams.append(i)
   # return filtered_bigrams

# print(filtered_bigrams)


freq_psychic = FreqDist(bigrams_psychic)
freq_skeptic = FreqDist(bigrams_skeptic)




# filter out start tokens in frequency data
def start_tokens_lst(frequency_data):
    return [i for i in frequency_data if i[0] == '<s>']


starting_tokens_psychic = start_tokens_lst(freq_psychic)
starting_tokens_skeptic = start_tokens_lst(freq_skeptic)



def generate_start_token(starting_tokens):
    return random.choice(starting_tokens)


# values_lst = [i for i in freq_bi.values()]


def generate_string_by_freq(freq_bi, starting_tokens):
    start = generate_start_token(starting_tokens)
    string = start
    update = start
    counter = 50
    while counter > 0:
        items_lst = [freq_bi[i] for i in freq_bi if i[0] == update[1]]
        max_value = max(items_lst)
        lst = [i for i in freq_bi if i[0] == update[1]]
        if counter % 2 == 0:
                append_item = random.choice([i for i in freq_bi if i[0] == update[1] and freq_bi[i] == max_value])
        else:
            append_item = random.choice([i for i in freq_bi if i[0] == update[1]])
        string = string + append_item
        if append_item[1] == '</s>':
            update = random.choice(starting_tokens)
        else:
            update = append_item
        counter = counter - 1
    output = list(string)
    return " ".join(output[1:][::2])

print(generate_string_by_freq(freq_psychic, starting_tokens_psychic))
print(generate_string_by_freq(freq_skeptic, starting_tokens_skeptic))



