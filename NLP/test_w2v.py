from gensim.models import Word2Vec
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.patches import Circle
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)

model = Word2Vec.load('twitch_corpus.wv')

all_words = np.zeros((len(model.wv.vocab),200))

print model.wv.most_similar(positive=['brock','pokemon'])

for idx,word in enumerate(model.wv.vocab.keys()):
    all_words[idx] = model.wv.word_vec(word,use_norm=True)

pca = PCA(n_components=2)
transformed = pca.fit_transform(all_words)

fig, ax = plt.subplots()

plt.scatter(transformed[:,0],transformed[:,1],s=1,alpha=0.3)

draw_arr = [['images/Kappa.png',[0.34437689 , 0.0151098],0.04],
           ['images/keepo.png',[0.39436573 ,-0.00743822],0.2],
           ['images/uber.png',[0.28720692 , 0.21862337],0.08],
           ['images/kappapride.png',[0.25727164, -0.07599034],0.03],
           ['images/kappaross.png',[0.31511026 , 0.05091153],0.06],
           ['images/dota.png',[0.25500367 , 0.1810048],0.04],
           ['images/clinton.png',[0.18837122 , 0.02360937],0.08],
           ['images/frankerz.png',[0.23220635, -0.0181457],0.14],
           ['images/greninja.png',[ 0.05229904, -0.00773189],0.18],
           ['images/hearthstone.png',[0.26097209,  0.16936783],0.13],
           ['images/heyguys.png',[ 0.21943741, -0.10263642],0.25],
           ['images/kreygasm.png',[ 0.33864356, -0.02364512],0.4],
           ['images/residentsleeper.png',[  0.20246886 , 0.0309899],0.1],
           ['images/biblethump.png',[ 0.2210096,  -0.03724498],0.08],
           ['images/maplestory.png',[0.21836475,  0.0846037],0.08],
           ['images/overwatch.png',[0.24811478,  0.21287289],0.1],
           ['images/pikachu.png',[0.30626137,  0.19531028],0.15],
           ['images/bulbasaur.png',[0.4133082 ,  0.17770401],0.04],
           ['images/h1z1.png',[0.28249365 , 0.27335746],0.12],
           ['images/pogchamp.png',[0.26069601, -0.03338625],0.2],
           ['images/pubg.png',[0.20866912,  0.26760333],0.01],
           ['images/runescape.png',[0.39874251,  0.0436783],0.12],
           ['images/trihard.png',[0.12390923, -0.02787331],0.05],
           ['images/sc2.png',[0.34643293,  0.2904229],0.13],
           ['images/trump.png',[0.13135138,  0.04047203],0.06],
           ['images/bernie.png',[0.15581421 , 0.03879099],0.033],
           ['images/obama.png',[0.1761705 , 0.03811327],0.18],
           ['images/bieber.png',[0.1402774 , 0.0836099],0.18],
           ['images/twitch.png',[0.2309821 ,  0.12904553],0.09],
           ['images/twitter.png',[0.22234173 , 0.11028058],0.02],
           ['images/xd.png',[0.32175036 , 0.0785713 ],0.1],
           ['images/panthers.png',[0.26076678 , 0.09306813 ],0.25],
           ['images/ttours.png',[0.22408171 , 0.0146354 ],0.08],
           ['images/luigi.png',[0.15099682 , 0.13665564 ],0.12],
           ['images/koopa.png',[0.35209905 , 0.12051587 ],0.08],
           ['images/ttours.png',[0.22408171 , 0.0146354 ],0.08],
           ['images/oot.png',[0.37905217 , 0.25971971],0.1],
           ['images/mtg.png',[0.37814827 , 0.17806543],0.16],
           ['images/mario.png',[0.25418041,  0.18055017],0.12],
           ['images/fortnite.png',[0.14911629 , 0.28644011],0.03],
           ['images/zelda.png',[0.27315091,  0.23038501],0.06]]

for img_name,xy,zoom in draw_arr:

    arr_img = plt.imread(img_name, format='png')

    imagebox = OffsetImage(arr_img, zoom=zoom)
    imagebox.image.axes = ax

    bbox_props = dict(lw=0)
    ab = AnnotationBbox(imagebox, xy,
                    xybox=(0., 0.),
                    frameon=False,
                    xycoords='data',
                    boxcoords="offset points",
                    pad=0.0)
    ax.add_artist(ab)

ax.set_xlim(0.1, 0.43)
ax.set_ylim(-0.12, 0.32)

plt.axis('off')
#plt.show()
plt.savefig('out.png',dpi=1000)
plt.close()

words = ['man','kappa','you','2mghype','frankerz','pogchamp','trihard',
         'biblethump','cmonbruh','kreygasm','kappapride','residentsleeper',
         'heyguys','runescape','pikachu','greninja','brock','guzma','dota',
         'pubg','league','overwatch','mario','hearthstone','zelda','gta',
         'maplestory','gretchen','trump','nigga','clinton','aspic','thrones',
         'spaghetti','titties','concerndoge','tarheels','aaaaeaaiau','sc',
         'panthers','hermione','swift','perry','gaga','cupcake','avril',
         'skirt','shirt','shibe','shiba','tswift','ttours','tentacle',
         'obama','poker','farmville','blackjack','objection','phoenix',
         'usa','mexico','canada','america','russia','uber','lyft','google',
         'twitch','amazon','twitter','netflix','codex','felicia','majora',
         'valkyrie','thor','odin','loki','ironman','spiderman','batman',
         'password','hughmungus','keepo','yangus','jcarver','ringabel','tiz',
         'edea','airy','xd','d','3','hatoful','auf','bieber','belieber',
         'arianator','harambe','bernie','kappaross','bulbasaur','h1z1','metro',
         'raichu','zapdos','mewtwo','groudon','kirby','mew','gardevoir',
         'garbodor','sableye','golisopod','lucario','lemmy','luigi','waluigi',
         'bowser','koopa','csgo','fortnite','wow','sw','jedi','windu','yoda','yoga'
         'sith','rogue','fifa','diablo','mtg','binding','sims','oot']

for word in words:
    if word in model.wv.vocab.keys():
        print word,model.wv.most_similar(positive=[word]),model.wv.most_similar(negative=[word])
        print pca.transform([model.wv.word_vec(word,use_norm=True)])

print model.wv.most_similar(positive=['frankerz','kappaross'],negative=['kappa'])
print model.wv.most_similar(positive=['kappa','concerndoge'],negative=['frankerz'])
print model.wv.most_similar(positive=['man','queen'],negative=['woman'])
print model.wv.most_similar(positive=['raichu','spearow'],negative=['pikachu'])
print model.wv.most_similar(positive=['luigi','bad'])
print model.wv.most_similar(positive=['waluigi','good'],negative=['bad'])
print model.wv.most_similar(positive=['waluigi','mario'],negative=['luigi'])
print model.wv.most_similar(positive=['waluigi','clinton'],negative=['luigi'])
print model.wv.most_similar(positive=['waluigi','hillary'],negative=['luigi'])
print model.wv.most_similar(positive=['clinton','good'],negative=['bad'])
print model.wv.most_similar(positive=['hillary','good'],negative=['bad'])

             
