from music21 import *
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
import re

environment.set('musicxmlPath', '/home/dominika/Pobrane/MuseScore-3.4.2-x86_64.AppImage')
#s.show()

#ilosc danych do analizy
print(len(corpus.getComposer('bach')))
print(len(corpus.getComposer('palestrina')))
#print(len(corpus.getComposer('ryansMammoth')))


for composer in ('bach','palestrina'):
    liczby_nut = []
    liczby_parti = []
    dlugosci_utworow = []
    metrum = []
    liczby_uzytych_metrum = []
    liczby_uzytych_tonacji = []
    najwyzsze_dzwieki = []
    najnizsze_dzwieki = []
    dokladnosci_tonacji = []
    rozstawy_dzwiekow = []
    pauzy = []

    i=0
    for title in corpus.corpora.CoreCorpus().search(composer, 'composer'):

        i = i+1
        if i==10:
            break
        liczby_nut.append(title.metadata.noteCount)
        liczby_parti.append(title.metadata.numberOfParts)
        dlugosci_utworow.append(title.metadata.quarterLength)
        metrum.append(title.metadata.timeSignatureFirst)
        liczby_uzytych_metrum.append(len(title.metadata.timeSignatures))
        liczby_uzytych_tonacji.append(len(title.metadata.keySignatures))
        najwyzsze_dzwieki.append(pitch.Pitch(title.metadata.pitchHighest).midi)
        najnizsze_dzwieki.append(pitch.Pitch(title.metadata.pitchLowest).midi)

        piece = corpus.parse(title)

        pauzy.append(len(piece.flat.getElementsByClass('Rest')))

        key = piece.analyze('key')
        dokladnosci_tonacji.append(key.correlationCoefficient)

        amb = str(piece.analyze('ambitus'))  #max rozstaw dzwiekow
        result = re.search("<\S+ \S(\d+)>",amb)
        rozstawy_dzwiekow.append(result.group(1))

        #inwersje akordów
        #liczba dzwiekow spoza tonacji
        #dynamika
        #rozlozenie dzwiekow (grafy)

    d = { 'liczby_nut' : liczby_nut, 'liczby_parti': liczby_parti,
          'dlugosci_utworow': dlugosci_utworow, 'metrum': metrum,
          'liczby_uzytych_metrum': liczby_uzytych_metrum,
            'liczby_uzytych_tonacji': liczby_uzytych_tonacji,
            'najwyzsze_dzwieki': najwyzsze_dzwieki, 'najnizsze_dzwieki': najnizsze_dzwieki,
            'dokladnosci_tonacji': dokladnosci_tonacji, 'rozstawy_dzwiekow': rozstawy_dzwiekow,
            'pauzy': pauzy}
    D = DataFrame(d)
    print(D)

