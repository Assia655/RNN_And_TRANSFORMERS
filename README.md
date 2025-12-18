# TP Part 1 : Traitement NLP Texte Arabe et Modèles Sequentiels

### Objectif général
Cet exercice combine le web scraping, le traitement du langage naturel arabe, et l'entraînement de modèles de deep learning pour prédire la pertinence (score) de textes arabes basée sur leur contenu.

---

## Étape 1 : Collecte de données (Web Scraping)

### Ce qu'on a fait
- Scraper plusieurs sites web arabes sur un sujet spécifique
- Collecter des textes arabes et leur attribuer un score de pertinence de 0 à 10

## Étape 2 : Pipeline de Prétraitement NLP

### Processus appliqué au texte arabe

1. **Normalisation** : Uniformiser le texte
   - Supprimer les voyelles arabes diacritiques
   - Normaliser les variantes de certaines lettres (أ إ آ → ا)
   - Supprimer les caractères non arabes

2. **Tokenization** : Découper le texte en mots individuels
   - "النص الأول" → ["النص", "الأول"]

3. **Suppression des stopwords** : Enlever les mots vides
   - Mots comme "في", "من", "و", "أو" n'ont pas de sens utile
   - Les supprimer pour garder les mots importants

4. **Stemming** : Réduire les mots à leur racine
   - "والمدرسة" → "مدرس"
   - Enlever les préfixes (ال, و, ب, ك, ل)
   - Enlever les suffixes (ها, ان, ات, ون, ين)

5. **Extraction de features** : Récupérer des caractéristiques
   - Nombre de mots
   - Nombre de caractères
   - Diversité lexicale

## Étape 3 : Entraînement des modèles

### Les 4 architectures testées

1. **RNN (Recurrent Neural Network)** 
   - Architecture basique récurrente
   - Traite les séquences en gardant une mémoire du passé

2. **BiRNN (Bidirectional RNN)**
   - Traite le texte dans les deux directions (avant et arrière)
   - Comprend mieux le contexte

3. **GRU (Gated Recurrent Unit)**
   - Version simplifiée du LSTM
   - Plus rapide à entraîner

4. **LSTM (Long Short-Term Memory)**
   - Architecture plus puissante avec gates spécialisés
   - Meilleure capture des dépendances à long terme

### Hyper-paramètres
- Embedding dimension : 128
- Hidden dimension : 128
- Epochs : 10
- Learning rate : adaptatif

---

## Résultats d'entraînement

### RNN
```
Epoch 1  | Train MSE: 0.4928 | Val MSE: 0.2522
Epoch 5  | Train MSE: 0.0286 | Val MSE: 0.1077
Epoch 10 | Train MSE: 0.0275 | Val MSE: 0.1038
```
- Convergence lente
- Performance moyenne

### BiRNN
```
Epoch 1  | Train MSE: 0.4210 | Val MSE: 0.1687
Epoch 5  | Train MSE: 0.0186 | Val MSE: 0.0749
Epoch 10 | Train MSE: 0.0068 | Val MSE: 0.0729
```
- Meilleure convergence que RNN
- MSE validation plus bas

### GRU
```
Epoch 1  | Train MSE: 0.5121 | Val MSE: 0.2456
Epoch 5  | Train MSE: 0.0198 | Val MSE: 0.0785
Epoch 10 | Train MSE: 0.0307 | Val MSE: 0.0742
```
- Performance intermédiaire

### LSTM
```
Epoch 1  | Train MSE: 0.4895 | Val MSE: 0.2289
Epoch 5  | Train MSE: 0.0241 | Val MSE: 0.0769
Epoch 10 | Train MSE: 0.0275 | Val MSE: 0.0738
```
- Très stable
- Bonne performance

---

## Étape 4 : Évaluation des modèles

### Métriques utilisées

1. **MSE (Mean Squared Error)** : Erreur quadratique moyenne
   - Plus bas = mieux
   - Pénalise les grandes erreurs

2. **MAE (Mean Absolute Error)** : Erreur absolue moyenne
   - Plus bas = mieux
   - Plus interprétable (en unités de score)

3. **R² (Coefficient de détermination)** : Qualité du modèle
   - Entre -∞ et 1
   - 1 = parfait, 0 = modèle banal, < 0 = très mauvais

### Résultats finaux

| Modèle | MSE     | MAE     | R²       |
|--------|---------|---------|----------|
| RNN    | 0.0677  | 0.1463  | -0.2329  |
| BiRNN  | 0.0676  | 0.1809  | -0.2307  |
| GRU    | 0.0698  | 0.1539  | -0.2708  |
| **LSTM** | **0.0647** | **0.1309** | **-0.1774** |

---


# TP Part 2 : Fine-tuning GPT-2 et Génération de Texte

### Objectif général
Cet exercice consiste à prendre un modèle de langage pré-entraîné (GPT-2) et l'adapter à un domaine spécifique en l'entraînant sur des données personnalisées, puis à l'utiliser pour générer du texte nouveau.

### Les trois étapes principales

**1. Créer un Dataset personnalisé**
- Générer ou utiliser vos propres textes (dans notre cas, des phrases sur l'intelligence artificielle et le machine learning)
- Ces textes servent de données d'entraînement pour adapter le modèle à votre domaine

**2. Fine-tuner GPT-2**
- Prendre le modèle pré-entraîné GPT-2 (déjà formé sur d'énormes quantités de texte)
- L'entraîner à nouveau sur votre dataset personnalisé pendant quelques epochs
- Cela permet au modèle d'apprendre les spécificités de votre domaine

**3. Générer du texte**
- Utiliser le modèle fine-tuné pour créer du texte nouveau
- Donner un "prompt" (une phrase de départ) et le modèle génère la suite
- Le modèle utilise ce qu'il a appris pour continuer de manière cohérente

---

## Résultats obtenus

```
Utilisation du device : cpu

✓ Dataset créé : custom_dataset.txt
✓ Modèle chargé

Démarrage du fine-tuning (3 epochs)...

Epoch 1/3: Loss moyen = 3.1746
Epoch 2/3: Loss moyen = 0.9148
Epoch 3/3: Loss moyen = 0.8072

✓ Modèle sauvegardé dans ./gpt2_finetuned
```

### Interprétation des résultats

- **Loss (perte)** : Mesure l'erreur du modèle
  - Epoch 1 : 3.17 (élevée - le modèle commence tout juste)
  - Epoch 2 : 0.91 (diminue - le modèle apprend)
  - Epoch 3 : 0.81 (baisse continue - bonne convergence)

- **La tendance** : La loss diminue à chaque epoch ✓ C'est bon signe, le modèle apprend correctement

- **Device utilisé** : CPU (traitement sur processeur, plus lent qu'un GPU mais fonctionnel)

---

## Conclusion

L'exercice a réussi. Le modèle GPT-2 a été :
- ✓ Téléchargé et chargé
- ✓ Entraîné sur les données personnalisées (3 epochs)
- ✓ Sauvegardé pour utilisation future
- ✓ Prêt à générer du texte basé sur vos prompts

Les avertissements affichés sont normaux et n'affectent pas le bon fonctionnement du programme.