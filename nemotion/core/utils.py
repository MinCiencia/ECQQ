import numpy as np
import pandas as pd

def get_closest_vector(pivots, names, emo_vector, embedding):
    words = []
    classes = []
    for w in emo_vector:
        v = embedding[w]
        mindist = 99999
        label = ''
        for p, n in zip(pivots, names):
            dist = np.linalg.norm(v-p)
            if dist < mindist:
                mindist = dist
                label = n
        words.append(w)
        classes.append(label)

    df = pd.DataFrame()
    df['word'] = words
    df['label'] = classes

    return df

def topics_per_document(model, corpus, start=0, end=1):
    corpus_sel = corpus[start:end]
    dominant_topics = []
    topic_percentages = []
    for i, corp in enumerate(corpus_sel):
        topic_percs, wordid_topics, wordid_phivalues = model[corp]
        dominant_topic = sorted(topic_percs, key = lambda x: x[1], reverse=True)[0][0]
        dominant_topics.append((i, dominant_topic))
        topic_percentages.append(topic_percs)
    return(dominant_topics, topic_percentages)


# dominant_topics, topic_percentages = topics_per_document(model=lda_model, corpus=corpus, end=-1)
# # Distribution of Dominant Topics in Each Document
# df = pd.DataFrame(dominant_topics, columns=['Document_Id', 'Dominant_Topic'])
# dominant_topic_in_each_doc = df.groupby('Dominant_Topic').size()
# df_dominant_topic_in_each_doc = dominant_topic_in_each_doc.to_frame(name='count').reset_index()
# # Total Topic Distribution by actual weight
# topic_weightage_by_doc = pd.DataFrame([dict(t) for t in topic_percentages])
# df_topic_weightage_by_doc = topic_weightage_by_doc.sum().to_frame(name='count').reset_index()


# from matplotlib.ticker import FuncFormatter
# # Plot
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 4), dpi=120, sharey=True)
# # Topic Distribution by Dominant Topics
# ax1.bar(x='Dominant_Topic', height='count', data=df_dominant_topic_in_each_doc, width=.5, color='firebrick')
# ax1.set_xticks(range(df_dominant_topic_in_each_doc.Dominant_Topic.unique().__len__()))

# ax1.set_title('Número de Documentos por Tópico Dominante', fontdict=dict(size=10))
# ax1.set_ylabel('Número de Documentos')
# ax1.set_ylim(0, 1000)
# # Topic Distribution by Topic Weights
# ax2.bar(x='index', height='count', data=df_topic_weightage_by_doc, width=.5, color='steelblue')
# ax2.set_xticks(range(df_topic_weightage_by_doc.index.unique().__len__()))
# ax2.set_title('Número de Documentos por Peso de los Tópicos', fontdict=dict(size=10))
# plt.show()

# diferencia=abs(df_dominant_topic_in_each_doc['count']-df_topic_weightage_by_doc['count'])
# divergencia.append(diferencia.sum()/df_dominant_topic_in_each_doc['count'].sum()

# # Show graph
# limit=30; start=2; step=1;
# x = range(start, limit, step)
# y = list(x)
# y=[((k-1)/k*2) for k in y]
# res = [i / j for i, j in zip(divergencia, y)]

# fig, ax1 = plt.subplots()
# color='steelblue'
# ax1.set_xlabel('Número de Tópicos de Necesidades')
# ax1.set_ylabel('Coherencia', color=color)
# ax1.plot(x, coherence_values, color=color)
# ax1.tick_params(axis='y', labelcolor=color)
# ax2 = ax1.twinx()
# color='firebrick'
# ax2.set_ylabel('Sesgo Mayoría Corregido', color=color)
# ax2.plot(x, res, color=color)
# ax2.tick_params(axis='y', labelcolor=color)
# fig.tight_layout()
# #plt.legend(("valor de coherencia", "sesgo mayoría"), loc='best')
# plt.show()
# fig.savefig('nece_num_topico_corr.pdf')