# attention_based_translation.py
# -*- coding: utf-8 -*-
"""Attention Based Translation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eaG-VOa_AABpYTHEyaHr-F-z0YQMQbY1
"""
from __future__ import unicode_literals, print_function, division
from io import open
import unicodedata
import re
import random

import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
import matplotlib.pyplot as plt

import numpy as np
from torch.utils.data import TensorDataset, DataLoader, RandomSampler

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# print(device)

SOS_token = 0
EOS_token = 1


class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: "SOS", 1: "EOS"}
        self.n_words = 2  # Count SOS and EOS

    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1


# Turn a Unicode string to plain ASCII, thanks to
# https://stackoverflow.com/a/518232/2809427
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


# Lowercase, trim, and remove non-letter characters
def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z!?]+", r" ", s)
    return s.strip()


# Lowercase, trim, and remove non-letter characters
def normalizeString(s):
    # Nweh and English vocabularies
    nweh_vocab = [
        # Basic characters and punctuation
        ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', 'ˌ',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', '<', '=', '>', '?',

        # Uppercase letters
        'A', 'B', 'C', 'D', 'E', 'Ə', 'Ɛ', 'F', 'G', 'GH', 'H', 'I', 'J', 'K', 'KH', 'L', 'M', 'N', 'Ŋ', 'O', 'Ɔ', 'P',
        'PF', 'R', 'S', 'T', 'TS', 'U', 'Ʉ', 'V', 'W', 'Y', 'Z',

        # Lowercase letters
        'a', 'b', 'c', 'd', 'e', 'ə', 'ε', 'f', 'g', 'gh', 'h', 'i', 'j', 'k', 'kh', 'l', 'm', 'n', 'ŋ', 'o', 'ɔ', 'p',
        'pf', 'r', 's', 't', 'ts', 'u', 'ʉ', 'v', 'w', 'y', 'z',

        # Consonant combinations
        'br', 'gb', 'kp', 'ny',

        # Vowels with tones
        'à', 'è', 'ù', 'ò', 'ʉ̀',  # Low tone
        'â', 'ê', 'û', 'ô', 'ʉ̂',  # Falling tone
        'ǎ', 'ě', 'ǔ', 'ǒ', 'ʉ̌',  # Rising tone
        'ā', 'ē', 'ū', 'ō', 'ʉ̄',  # Level or mid tone
        'á', 'é', 'í', 'ó', 'ú', 'ʉ́',  # High tone

        # Special characters
        'ɑ', 'ɓ', 'ɗ', 'ɨ',

        # Tonal variations
        'à', 'á', 'ā', 'â', 'ǎ',
        'ɑ̀', 'ɑ́', 'ɑ̄', 'ɑ̂', 'ɑ̌',
        'è', 'é', 'ē', 'ê', 'ě',
        'ə̀', 'ə́', 'ə̄', 'ə̂', 'ə̌',
        'ɛ̀', 'έ', 'ɛ̄', 'ɛ̂', 'ɛ̌',
        'ì', 'í', 'ī', 'î', 'ǐ',
        'ò', 'ó', 'ō', 'ô', 'ǒ',
        'ɔ̀', 'ɔ́', 'ɔ̄', 'ɔ̂', 'ɔ̌',
        'ù', 'ú', 'ū', 'û', 'ǔ',
        'ʉ̀', 'ʉ́', 'ʉ̄', 'ʉ̂', 'ʉ̌',
        'ŋ̀', 'ŋ́', 'ŋ̄', 'ŋ̂', 'ŋ̌',

        # Double vowels
        'àà', 'áá', 'āā',
        'ɑ̀ɑ̀', 'ɑ́ɑ́', 'ɑ̄ɑ̄',
        'èè', 'éé', 'ēē',
        'ə̀ə̀', 'ə́ə́', 'ə̄ə̄',
        'ɛ̀ɛ̀', 'έέ', 'ɛ̄ɛ̄',
        'ìì', 'íí', 'īī',
        'òò', 'óó', 'ōō',
        'ɔ̀ɔ̀', 'ɔ́ɔ́', 'ɔ̄ɔ̄',
        'ùù', 'úú', 'ūū',
        'ʉ̀ʉ̀', 'ʉ́ʉ́', 'ʉ̄ʉ̄',

        # Mixed tone double vowels
        'ìà', 'íá', 'īā',
        'ìɑ̀', 'íɑ́', 'īɑ̄',
        'ìè', 'íé', 'īē',
        'ùà', 'úá', 'ūā'
    ]

    eng_vocab = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
                 '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', '<', '=', '>', '?', '@',
                 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                 'Y', 'Z', '[', '\\', ']', '^', '_', '`',
                 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                 'y', 'z', '{', '|', '}', '~']

    s = s.lower().strip()

    # Normalize unicode to ASCII for non-Nweh characters
    s = unicodeToAscii(s)

    # Create a set of allowed characters based on both vocabularies
    allowed_chars = set(nweh_vocab + eng_vocab)

    # Remove characters not in the allowed set
    s = ''.join(c for c in s if c in allowed_chars or unicodedata.category(c) != 'Mn')

    # Replace certain punctuation with space-punctuation-space for consistency
    s = re.sub(r"([.!?])", r" \1", s)

    return s.strip()


# Nweh and English vocabularies

def readLangs(lang1, lang2, reverse=False):
    # print("Reading lines...")

    # Read the file and split into lines
    lines = open('users/text_translation/data/train.txt',
                 encoding='utf-8'). \
        read().strip().split('\n')

    # Split every line into pairs and normalize
    pairs = [[normalizeString(s) for s in l.split('\t')] for l in lines]

    # Reverse pairs, make Lang instances
    if reverse:
        pairs = [list(reversed(p)) for p in pairs]
        input_lang = Lang(lang2)
        output_lang = Lang(lang1)
    else:
        input_lang = Lang(lang1)
        output_lang = Lang(lang2)

    return input_lang, output_lang, pairs


MAX_LENGTH = 20

eng_prefixes = (
    "i am ", "i m ",
    "he is", "he s ",
    "she is", "she s ",
    "you are", "you re ",
    "we are", "we re ",
    "they are", "they re "
)


def filterPair(p):
    return len(p[0].split(' ')) < MAX_LENGTH and \
        len(p[1].split(' ')) < MAX_LENGTH


def filterPairs(pairs):
    return [pair for pair in pairs if filterPair(pair)]


def prepareData(lang1, lang2, reverse=True):
    input_lang, output_lang, pairs = readLangs(lang1, lang2, reverse)
    # print("Read %s sentence pairs" % len(pairs))
    pairs = filterPairs(pairs)
    # print("Trimmed to %s sentence pairs" % len(pairs))
    # print("Counting words...")
    for pair in pairs:
        input_lang.addSentence(pair[0])
        output_lang.addSentence(pair[1])
    # print("Counted words:")
    # print(input_lang.name, input_lang.n_words)
    # print(output_lang.name, output_lang.n_words)
    return input_lang, output_lang, pairs


input_lang, output_lang, pairs = prepareData('nweh', 'english', True)


# print(random.choice(pairs))


class EncoderRNN(nn.Module):
    def __init__(self, input_size, hidden_size, dropout_p=0.1):
        super(EncoderRNN, self).__init__()
        self.hidden_size = hidden_size

        self.embedding = nn.Embedding(input_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size, batch_first=True)
        self.dropout = nn.Dropout(dropout_p)

    def forward(self, input):
        embedded = self.dropout(self.embedding(input))
        output, hidden = self.gru(embedded)
        return output, hidden


class DecoderRNN(nn.Module):
    def __init__(self, hidden_size, output_size):
        super(DecoderRNN, self).__init__()
        self.embedding = nn.Embedding(output_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size, batch_first=True)
        self.out = nn.Linear(hidden_size, output_size)

    def forward(self, encoder_outputs, encoder_hidden, target_tensor=None):
        batch_size = encoder_outputs.size(0)
        decoder_input = torch.empty(batch_size, 1, dtype=torch.long, device=device).fill_(SOS_token)
        decoder_hidden = encoder_hidden
        decoder_outputs = []

        for i in range(MAX_LENGTH):
            decoder_output, decoder_hidden = self.forward_step(decoder_input, decoder_hidden)
            decoder_outputs.append(decoder_output)

            if target_tensor is not None:
                # Teacher forcing: Feed the target as the next input
                decoder_input = target_tensor[:, i].unsqueeze(1)  # Teacher forcing
            else:
                # Without teacher forcing: use its own predictions as the next input
                _, topi = decoder_output.topk(1)
                decoder_input = topi.squeeze(-1).detach()  # detach from history as input

        decoder_outputs = torch.cat(decoder_outputs, dim=1)
        decoder_outputs = F.log_softmax(decoder_outputs, dim=-1)
        return decoder_outputs, decoder_hidden, None  # We return `None` for consistency in the training loop

    def forward_step(self, input, hidden):
        output = self.embedding(input)
        output = F.relu(output)
        output, hidden = self.gru(output, hidden)
        output = self.out(output)
        return output, hidden


class BahdanauAttention(nn.Module):
    def __init__(self, hidden_size):
        super(BahdanauAttention, self).__init__()
        self.Wa = nn.Linear(hidden_size, hidden_size)
        self.Ua = nn.Linear(hidden_size, hidden_size)
        self.Va = nn.Linear(hidden_size, 1)

    def forward(self, query, keys):
        scores = self.Va(torch.tanh(self.Wa(query) + self.Ua(keys)))
        scores = scores.squeeze(2).unsqueeze(1)

        weights = F.softmax(scores, dim=-1)
        context = torch.bmm(weights, keys)

        return context, weights


class AttnDecoderRNN(nn.Module):
    def __init__(self, hidden_size, output_size, dropout_p=0.1):
        super(AttnDecoderRNN, self).__init__()
        self.embedding = nn.Embedding(output_size, hidden_size)
        self.attention = BahdanauAttention(hidden_size)
        self.gru = nn.GRU(2 * hidden_size, hidden_size, batch_first=True)
        self.out = nn.Linear(hidden_size, output_size)
        self.dropout = nn.Dropout(dropout_p)

    def forward(self, encoder_outputs, encoder_hidden, target_tensor=None):
        batch_size = encoder_outputs.size(0)
        decoder_input = torch.empty(batch_size, 1, dtype=torch.long, device=device).fill_(SOS_token)
        decoder_hidden = encoder_hidden
        decoder_outputs = []
        attentions = []

        for i in range(MAX_LENGTH):
            decoder_output, decoder_hidden, attn_weights = self.forward_step(
                decoder_input, decoder_hidden, encoder_outputs
            )
            decoder_outputs.append(decoder_output)
            attentions.append(attn_weights)

            if target_tensor is not None:
                # Teacher forcing: Feed the target as the next input
                decoder_input = target_tensor[:, i].unsqueeze(1)  # Teacher forcing
            else:
                # Without teacher forcing: use its own predictions as the next input
                _, topi = decoder_output.topk(1)
                decoder_input = topi.squeeze(-1).detach()  # detach from history as input

        decoder_outputs = torch.cat(decoder_outputs, dim=1)
        decoder_outputs = F.log_softmax(decoder_outputs, dim=-1)
        attentions = torch.cat(attentions, dim=1)

        return decoder_outputs, decoder_hidden, attentions

    def forward_step(self, input, hidden, encoder_outputs):
        embedded = self.dropout(self.embedding(input))

        query = hidden.permute(1, 0, 2)
        context, attn_weights = self.attention(query, encoder_outputs)
        input_gru = torch.cat((embedded, context), dim=2)

        output, hidden = self.gru(input_gru, hidden)
        output = self.out(output)

        return output, hidden, attn_weights


def indexesFromSentence(lang, sentence):
    # Check if sentence is None or empty to avoid AttributeError
    if not sentence:
        return []
    words = []
    # Split the sentence into words and get their indexes
    for word in sentence.split(' '):
        words.append(lang.word2index.get(word, 0))
    return words


def tensorFromSentence(lang, sentence):
    indexes = indexesFromSentence(lang, sentence)
    indexes.append(EOS_token)
    return torch.tensor(indexes, dtype=torch.long, device=device).view(1, -1)


def tensorsFromPair(pair):
    input_tensor = tensorFromSentence(input_lang, pair[0])
    target_tensor = tensorFromSentence(output_lang, pair[1])
    return (input_tensor, target_tensor)


def get_dataloader(batch_size):
    input_lang, output_lang, pairs = prepareData('eng', 'nweh', True)

    n = len(pairs)
    input_ids = np.zeros((n, MAX_LENGTH), dtype=np.int32)
    target_ids = np.zeros((n, MAX_LENGTH), dtype=np.int32)

    for idx, (inp, tgt) in enumerate(pairs):
        inp_ids = indexesFromSentence(input_lang, inp)
        tgt_ids = indexesFromSentence(output_lang, tgt)
        inp_ids.append(EOS_token)
        tgt_ids.append(EOS_token)
        input_ids[idx, :len(inp_ids)] = inp_ids
        target_ids[idx, :len(tgt_ids)] = tgt_ids

    train_data = TensorDataset(torch.LongTensor(input_ids).to(device),
                               torch.LongTensor(target_ids).to(device))

    train_sampler = RandomSampler(train_data)
    train_dataloader = DataLoader(train_data, sampler=train_sampler, batch_size=batch_size)
    return input_lang, output_lang, train_dataloader


def train_epoch(dataloader, encoder, decoder, encoder_optimizer,
                decoder_optimizer, criterion):
    total_loss = 0
    for data in dataloader:
        input_tensor, target_tensor = data

        encoder_optimizer.zero_grad()
        decoder_optimizer.zero_grad()

        encoder_outputs, encoder_hidden = encoder(input_tensor)
        decoder_outputs, _, _ = decoder(encoder_outputs, encoder_hidden, target_tensor)

        loss = criterion(
            decoder_outputs.view(-1, decoder_outputs.size(-1)),
            target_tensor.view(-1)
        )
        loss.backward()

        encoder_optimizer.step()
        decoder_optimizer.step()

        total_loss += loss.item()

    return total_loss / len(dataloader)


import time
import math


def asMinutes(s):
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)


def timeSince(since, percent):
    now = time.time()
    s = now - since
    es = s / (percent)
    rs = es - s
    return '%s (- %s)' % (asMinutes(s), asMinutes(rs))


def train(train_dataloader, encoder, decoder, n_epochs, learning_rate=0.001,
          print_every=100, plot_every=100):
    start = time.time()
    plot_losses = []
    print_loss_total = 0  # Reset every print_every
    plot_loss_total = 0  # Reset every plot_every

    encoder_optimizer = optim.Adam(encoder.parameters(), lr=learning_rate)
    decoder_optimizer = optim.Adam(decoder.parameters(), lr=learning_rate)
    criterion = nn.NLLLoss()

    for epoch in range(1, n_epochs + 1):
        loss = train_epoch(train_dataloader, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion)
        print_loss_total += loss
        plot_loss_total += loss

        if epoch % print_every == 0:
            print_loss_avg = print_loss_total / print_every
            print_loss_total = 0
            print('%s (%d %d%%) %.4f' % (timeSince(start, epoch / n_epochs),
                                         epoch, epoch / n_epochs * 100, print_loss_avg))

        if epoch % plot_every == 0:
            plot_loss_avg = plot_loss_total / plot_every
            plot_losses.append(plot_loss_avg)
            plot_loss_total = 0

    # showPlot(plot_losses)


# Commented out IPython magic to ensure Python compatibility.


# %matplotlib inline
plt.switch_backend('agg')
import matplotlib.ticker as ticker
import numpy as np


def showPlot(points):
    plt.figure()
    fig, ax = plt.subplots()
    # this locator puts ticks at regular intervals
    loc = ticker.MultipleLocator(base=0.2)
    ax.yaxis.set_major_locator(loc)
    # plt.plot(points)
    # plt.savefig("./img/losses.png")


def evaluate(encoder, decoder, sentence, input_lang, output_lang):
    with torch.no_grad():
        input_tensor = tensorFromSentence(input_lang, sentence)

        encoder_outputs, encoder_hidden = encoder(input_tensor)
        decoder_outputs, decoder_hidden, decoder_attn = decoder(encoder_outputs, encoder_hidden)

        _, topi = decoder_outputs.topk(1)
        decoded_ids = topi.squeeze()

        decoded_words = []
        for idx in decoded_ids:
            if idx.item() == EOS_token:
                decoded_words.append('<EOS>')
                break
            decoded_words.append(output_lang.index2word[idx.item()])
    return decoded_words, decoder_attn


def evaluateRandomly(encoder, decoder, n=10):
    for i in range(n):
        pair = random.choice(pairs)
        # print('>', pair[0])
        # print('=', pair[1])
        output_words, _ = evaluate(encoder, decoder, pair[0], input_lang, output_lang)
        output_sentence = ' '.join(output_words)
        # print('<', output_sentence)
        # print('')


hidden_size = 128
batch_size = 512

input_lang, output_lang, train_dataloader = get_dataloader(batch_size)

encoder = EncoderRNN(input_lang.n_words, hidden_size).to(device)
decoder = AttnDecoderRNN(hidden_size, output_lang.n_words).to(device)

# train(train_dataloader, encoder, decoder, 200, print_every=5, plot_every=5)

encoder.eval()
decoder.eval()
evaluateRandomly(encoder, decoder)


def showAttention(input_sentence, output_words, attentions):
    # fig = plt.figure(figsize=(15, 10))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(attentions.cpu().numpy(), cmap='bone')
    fig.colorbar(cax)

    # Set up axes
    # ax.set_xticklabels([''] + input_sentence.split(' ') +
    #                    ['<EOS>'], rotation=90)
    # ax.set_yticklabels([''] + output_words)

    # Show label at every tick
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    # Add labels
    # ax.set_xlabel('Input Sentence')
    # ax.set_ylabel('Output Words')
    # ax.set_title('Translation Quality Metrics', pad=20)
    # # Adjust the layout to accommodate the title and labels
    # plt.tight_layout(rect=[0, 0, 1, 0.95])
    # plt.savefig("./img/test.png")
    # plt.show()


def evaluateAndShowAttention(input_sentence):
    output_words, attentions = evaluate(encoder, decoder, input_sentence, input_lang, output_lang)
    # print('input =', input_sentence)
    # Join the output words into a single string, excluding the '<EOS>' token if present
    output_sentence = ' '.join(word for word in output_words if word != '<EOS>')
    # print('output =', output_sentence)
    showAttention(input_sentence, output_words, attentions[0, :len(output_words), :])
    return output_sentence


# torch.save(encoder.state_dict(), 'volingual_encoder.pt')
# torch.save(decoder.state_dict(), 'volingual_decoder.pt')
encoder.load_state_dict(torch.load('users/text_translation/volingual_encoder.pt'))
decoder.load_state_dict(torch.load('users/text_translation/volingual_decoder.pt'))
encoder.eval()
decoder.eval()

# def evaluateAndShowAttention(input_sentence):
#     hidden_size = 128
#     input_lang, output_lang, pairs = prepareData('nweh', 'english', True)
#     encoder = EncoderRNN(input_lang.n_words, hidden_size).to(device)
#     encoder.load_state_dict(torch.load(
#         '/home/unix/Documents/GitHub/Volingual/Backend/volingual/services/text_translation/volingual_encoder.pt'))
#     decoder = AttnDecoderRNN(hidden_size, output_lang.n_words).to(device)
#     decoder.load_state_dict(torch.load(
#         '/home/unix/Documents/GitHub/Volingual/Backend/volingual/services/text_translation/volingual_decoder.pt'))
#     encoder.eval()
#     decoder.eval()
#     output_words, attentions = evaluate(encoder, decoder, input_sentence, input_lang, output_lang)
#     # print('input =', input_sentence)
#     # print('output =', ' '.join(output_words))
#     showAttention(input_sentence, output_words, attentions[0, :len(output_words), :])
#     return ' '.join(output_words)


# evaluateAndShowAttention("Have you not built that house?")