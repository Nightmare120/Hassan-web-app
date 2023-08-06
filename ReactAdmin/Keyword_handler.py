import yake

# Input Text
# text = '''Full stack developer'''
# Specifying Parameters
language = "en"
max_ngram_size = 3
deduplication_thresold = 0.9
deduplication_algo = 'seqm'
windowSize = 1
numOfKeywords = 20

def get_keywords(text):
    all_keywords = []
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(text)

    for kw in keywords:
        # print(kw,type(kw))
        all_keywords.append(kw[0])

    return all_keywords

def get_conversation_with_keywords(conversation):
    # conversation = ["ok","Yes","21","Full stack developer"]
    conversation_with_keyword = []

    for response in conversation:
        data = {
            "res": response['txt'],
            "url": response['url'],
            "keywords": get_keywords( response['txt'])
        }
        print(get_keywords(response),end="\n\n\n")
        conversation_with_keyword.append(data)

    return conversation_with_keyword
    

