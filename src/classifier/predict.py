import json
from functools import lru_cache
from pathlib import Path
from typing import Dict, List

import joblib
import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from ..config import settings
from .constants import cat_cols, float_cols


@lru_cache
def load_files():

    model_path = Path(settings.MODEL_PATH)

    # Store the vectorizer as key, lightgbm model as value
    model_dict = dict()

    for item in model_path.iterdir():

        if item.is_dir():

            vect = joblib.load(item / 'tfidf.vec')
            lgb_model = lgb.Booster(model_file=(item / 'lgb.txt').as_posix())

            model_dict[vect] = lgb_model

    with open(model_path / 'label2id.json', 'r') as f:
        label2id = json.load(f)

    id2label = dict((v, k) for k, v in label2id.items())

    return model_dict, id2label


def predict_prob(
        df: pd.DataFrame,
        vect: TfidfVectorizer,
        model: lgb.Booster
) -> np.ndarray:

    x_tfidf = vect.transform(df['processed_tags']).toarray()
    x_float = df[float_cols].values
    x_cat = df[cat_cols].values

    x = np.column_stack([x_tfidf, x_float, x_cat])

    y_pred = model.predict(x)

    return y_pred


def predict_ensemble(
    df: pd.DataFrame,
    model_dict: Dict[TfidfVectorizer, lgb.Booster],
    id2label: Dict[int, str],
) -> List:

    num_class = len(id2label)
    y_pred_combined = np.zeros((len(df), num_class))

    for vect, model in model_dict.items():
        y_pred = predict_prob(df, vect, model)
        y_pred_combined += y_pred

    preds_idx = y_pred_combined.argmax(axis=1)
    preds_class = list(map(lambda x: id2label[x], preds_idx))

    return preds_class


MODEL_DICT, ID2LABEL = load_files()
